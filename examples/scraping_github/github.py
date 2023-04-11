"""
This file provides functions that make it easy to use github's api to extract things like stars,
forks, readme file, etc..
"""
import asyncio
from typing import Optional
import aiohttp
import requests
import re
from datetime import datetime


def clean_github_url(url: str) -> str:
    """
    Given a url to a github repo (e.g. `github.com/user/repo/master/etc.`), clean/standardize the
    URL (e.g. `github.com/user/repo`)
    """
    if not url:
        return None

    url = url.strip()
    # Define a regular expression pattern to match the domain and first two subdirectories
    pattern = r'.*(https?://github.com/[^/]+/?[^/]*)'
    # Use the re.match() function to extract the domain and first two subdirectories
    match = re.match(pattern, url)
    if not match:
        return None

    url = match.group(1).strip()
    url = re.sub(r'/$', '', url)
    url = re.sub(r'.git$', '', url)
    assert url
    return url


def extract_username_reponame(url: str) -> tuple[str]:
    """
    Givven a url (e.g. `github.com/user/repo`) extract the user-name and repo-name (e.g. `user` and
    `repo'). Returns a tuple (e.g. `('user', 'repo')`)
    """
    user_name = None
    repo_name = None

    if not url:
        return (user_name, repo_name)

    url = url.strip()
    # Define a regular expression pattern to match the domain and first two subdirectories
    pattern = r'^https?://github.com/([^/]+)/?([^/]*)'
    # pattern = r'^https'
    # Use the re.match() function to extract the domain and first two subdirectories
    import re
    match = re.match(pattern, url)
    if not match:
        return (user_name, repo_name)

    matches = match.groups()
    user_name = re.sub(r'/$', '', matches[0])

    if len(matches) > 1:
        repo_name = re.sub(r'/$', '', matches[1])
        repo_name = repo_name if repo_name else None

    return (user_name, repo_name)


async def get_github_metadata(
        session: aiohttp.ClientSession,
        user_name: str,
        repo_name: str) -> dict:
    """
    Given a user-name and repo-name, extracts metadata about the correpsonding repo (e.g. # of
    stars, # of forks, description, topics, etc.)
    """
    repo_url = f'https://api.github.com/repos/{user_name}/{repo_name}'
    results = dict(
        error=None,
        user_name=user_name,
        repo_name=repo_name,
        url=repo_url,
    )

    # if we know the user_name or repo_name is None or missing then let's not even attempt the
    # API call, since it will count against our rate limits
    if not user_name or not repo_name:
        results['error'] = 'missing user/repo'
        return results

    async with session.get(repo_url) as response:
        if response.status == 200:
            repo_metadata = await response.json()
            results['description'] = repo_metadata.get('description', None)
            owner = repo_metadata.get('owner', None)
            if owner:
                results['owner_login'] = owner.get('login', None)
                results['owner_type'] = owner.get('type', None)
            else:
                results['owner_login'] = None
                results['owner_type'] = None

            results['homepage'] = repo_metadata.get('homepage', None)
            results['topics'] = repo_metadata.get('topics', None)
            # https://github.com/orgs/community/discussions/24795
            # https://developer.github.com/changes/2012-09-05-watcher-api/
            results['subscribers_count'] = repo_metadata.get('subscribers_count', None)
            results['stargazers_count'] = repo_metadata.get('stargazers_count', None)
            results['forks_count'] = repo_metadata.get('forks_count', None)
            results['default_branch'] = repo_metadata.get('default_branch', None)
            results['archived'] = repo_metadata.get('archived', None)
            results['response_header'] = response.headers
        else:
            results['error'] = f"{response.status}: {response.reason}"
            results['response_header'] = response.headers

    return results


async def get_github_readme_url(
        session: aiohttp.ClientSession,
        user_name: str,
        repo_name: str) -> dict:
    """
    Given a user-name and repo-name, extracts the readme file's URL. This is necessary because
    readmes will have different extensions (e.g. `.md`, `.rst`, `.txt`).
    """
    repo_url = f'https://api.github.com/repos/{user_name}/{repo_name}/contents'
    results = dict(
        error=None,
        user_name=user_name,
        repo_name=repo_name,
        url=repo_url,
    )
    # if we know the user_name or repo_name is None or missing then let's not even attempt the
    # API call, since it will count against our rate limits
    if not user_name or not repo_name:
        results['error'] = 'missing user/repo'
        return results

    async with session.get(repo_url) as response:
        if response.status == 200:
            files = await response.json()
            readme_url = [f['download_url'] for f in files if 'readme.' in f['name'].lower()]
            if readme_url:
                readme_url = readme_url[0]
                results['readme_url'] = readme_url
            else:
                results['error'] = 'readme url not found'

            results['response_header'] = response.headers
            str(response.headers)
        elif response.status == 403:
            results['error'] = f"{response.status}: {response.reason}"
            results['response_header'] = response.headers
        else:
            results['error'] = f"{response.status}: {response.reason}"
            results['response_header'] = response.headers

    return results


async def get_github_readme_contents(session: aiohttp.ClientSession, url: str) -> dict:
    """
    Given a Github Readme URL, e.g.:

        https://raw.githubusercontent.com/apache/airflow/main/README.md

    this function extracts the contents of the file.
    """
    results = dict(
        error=None,
        url=url,
    )
    # if we know the url is None or missing then let's not even attempt the
    # API call, since it will count against our rate limits
    if not url:
        results['error'] = 'missing url'
        return results

    async with session.get(url) as response:
        if response.status == 200:
            contents = await response.text()
            results['readme'] = contents
            results['response_header'] = response.headers
        else:
            results['error'] = f"{response.status}: {response.reason}"
            results['response_header'] = response.headers

    return results


async def run_async(func: callable, param_kwargs: list[dict], token: Optional[str] = None) -> list:
    """
    This function is a simple wrapper around the logic needed to asynchronously run one of the
    async functions above (e.g. `get_github_metadata`).

    A token is required if making many calls in order to increase the rate limit.

    Args:
        func:
            The function to call asynchronously
            e.g. get_github_metadata, get_github_readme_url, get_github_readme_contents
        param_kwargs:
            parameter/values for corresponding func
            e.g. {'user_name': 'scikit-learn', 'repo_name': 'scikit-learn'}
        token:
            the github token to use (without it rate-limits are very low)
    """
    if token:
        headers = {'Authorization': f'Bearer {token}'}
    else:
        headers = None

    # connector = aiohttp.TCPConnector(limit_per_host=10)
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for params in param_kwargs:
            task = asyncio.ensure_future(func(session=session, **params))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results


def get_rate_limits(token: str) -> dict:
    """
    For a given token, this function returns a dict containing some basic information on rate
    limits (e.g. available, remaining)
    """
    url = 'https://api.github.com/rate_limit'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        result = dict(
            limit=data['rate']['limit'],
            remaining=data['rate']['remaining'],
            reset_time=datetime.fromtimestamp(data['rate']['reset']).isoformat(),
        )
        return result
    else:
        raise Exception(f'Request failed with status code {response.status_code}.')
