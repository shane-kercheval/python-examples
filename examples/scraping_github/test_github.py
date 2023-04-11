import os
from pathlib import Path
import aiohttp
import pytest
import github as gh


@pytest.fixture()
def github_token():
    with open(os.path.join(Path.home(), '.github_token'), 'r') as handle:
        contents = handle.read()
    return contents


def test__clean_github_url():
    assert gh.clean_github_url(r'https://github.com/huggingface/') == r'https://github.com/huggingface'  # noqa
    assert gh.clean_github_url(r'https://github.com/huggingface') == r'https://github.com/huggingface'  # noqa
    assert gh.clean_github_url(r'http://github.com/huggingface/datasets') == r'http://github.com/huggingface/datasets'  # noqa
    assert gh.clean_github_url(r'http://github.com/huggingface/datasets/test') == r'http://github.com/huggingface/datasets'  # noqa
    assert gh.clean_github_url(r'https://github.com/huggingface/datasets') == r'https://github.com/huggingface/datasets'  # noqa
    assert gh.clean_github_url(r'https://github.com/huggingface/datasets/test') == r'https://github.com/huggingface/datasets'  # noqa
    assert gh.clean_github_url(r'https://github.com/hugging-face/datasets') == r'https://github.com/hugging-face/datasets'  # noqa
    assert gh.clean_github_url(r'https://github.com/huggingface/data-sets') == r'https://github.com/huggingface/data-sets'  # noqa
    assert gh.clean_github_url(r'https://github.com/hugging-face/data-sets') == r'https://github.com/hugging-face/data-sets'  # noqa
    assert gh.clean_github_url(r'https://github.com/hugging-face/datasets/test') == r'https://github.com/hugging-face/datasets'  # noqa
    assert gh.clean_github_url(r'https://github.com/huggingface/data-sets/test') == r'https://github.com/huggingface/data-sets'  # noqa
    assert gh.clean_github_url(r'https://github.com/hugging-face/data-sets/test') == r'https://github.com/hugging-face/data-sets'  # noqa
    assert gh.clean_github_url(r'https://github.com/hugging-face/data-sets.git') == r'https://github.com/hugging-face/data-sets'  # noqa
    assert gh.clean_github_url(r'https://github.com/geopandas/geopandas/releases/download/v0.8.1/geopandas-0.8.1.tar.gz') == r'https://github.com/geopandas/geopandas'  # noqa
    assert gh.clean_github_url(r'http://toblerity.github.com/rtree/') is None  # noqa


def test__clean_github_url__multiple_urls():
    value = r'https://r-spatial.github.io/sf/, https://github.com/r-spatial/sf/'
    assert gh.clean_github_url(value) == r'https://github.com/r-spatial/sf'
    value = r'https://github.com/r-spatial/sf/, https://r-spatial.github.io/sf/'
    assert gh.clean_github_url(value) == r'https://github.com/r-spatial/sf'


def test__extract_username_reponame():
    assert gh.extract_username_reponame(r'https://github.com/huggingface/') == ('huggingface', None)  # noqa
    assert gh.extract_username_reponame(r'https://github.com/huggingface') == ('huggingface', None)  # noqa

    assert gh.extract_username_reponame(r'http://github.com/huggingface/datasets') == ('huggingface', 'datasets')  # noqa
    assert gh.extract_username_reponame(r'http://github.com/huggingface/datasets/test') == ('huggingface', 'datasets')  # noqa
    assert gh.extract_username_reponame(r'https://github.com/huggingface/datasets') == ('huggingface', 'datasets')  # noqa
    assert gh.extract_username_reponame(r'https://github.com/huggingface/datasets/test') == ('huggingface', 'datasets')  # noqa
    assert gh.extract_username_reponame(r'https://github.com/hugging-face/datasets') == ('hugging-face', 'datasets')  # noqa
    assert gh.extract_username_reponame(r'https://github.com/huggingface/data-sets') == ('huggingface', 'data-sets')  # noqa
    assert gh.extract_username_reponame(r'https://github.com/hugging-face/data-sets') == ('hugging-face', 'data-sets')  # noqa

    assert gh.extract_username_reponame(r'https://github.com/hugging-face/datasets/test') == ('hugging-face', 'datasets')  # noqa
    assert gh.extract_username_reponame(r'https://github.com/huggingface/data-sets/test') == ('huggingface', 'data-sets')  # noqa
    assert gh.extract_username_reponame(r'https://github.com/hugging-face/data-sets/test') == ('hugging-face', 'data-sets')  # noqa
    assert gh.extract_username_reponame(r'https://github.com/geopandas/geopandas/releases/download/v0.8.1/geopandas-0.8.1.tar.gz') == ('geopandas', 'geopandas')  # noqa

    assert gh.extract_username_reponame(r'http://toblerity.github.com/rtree/') == (None, None)  # noqa
    assert gh.extract_username_reponame(r'http://github.com/') == (None, None)  # noqa


@pytest.mark.asyncio
async def test__get_github_repo_info__non_existant_repo(github_token):
    user_name = 'non'
    repo_name = 'existant'
    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {github_token}'}) as session:  # noqa
        coroutine = gh.get_github_metadata(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == '404: Not Found'
    assert results['response_header'] is not None
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name


@pytest.mark.asyncio
async def test__get_github_repo_info__no_user_repo():
    # test with missing user_name
    user_name = None
    repo_name = 'existant'
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_metadata(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == 'missing user/repo'
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name

    # test with empty user_name
    user_name = ''
    repo_name = 'existant'
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_metadata(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == 'missing user/repo'
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name

    # test with missing repo_name
    user_name = 'non'
    repo_name = None
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_metadata(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == 'missing user/repo'
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name

    # test with empty repo_name
    user_name = 'non'
    repo_name = ''
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_metadata(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == 'missing user/repo'
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name

    # test with missing user_name and repo_name
    user_name = None
    repo_name = None
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_metadata(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == 'missing user/repo'
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name


@pytest.mark.asyncio
async def test__get_github_repo_info(github_token):
    user_name = 'apache'
    repo_name = 'airflow'

    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {github_token}'}) as session:  # noqa
        coroutine = gh.get_github_metadata(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    expected_key_subset = {'error', 'user_name', 'repo_name', 'owner_login', 'owner_type', 'url'}
    assert expected_key_subset < set(results.keys())
    assert results['error'] is None

    error_value = results.pop('error')
    assert error_value is None
    assert 'error' not in results.keys()
    assert all([x is not None for x in results.values()])
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}'
    assert results['stargazers_count'] > 29_000
    assert results['subscribers_count'] > 700
    assert results['forks_count'] > 10_000


@pytest.mark.asyncio
async def test__get_github_readme_url__non_existant_repo(github_token):
    user_name = 'non'
    repo_name = 'existant'
    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {github_token}'}) as session:  # noqa
        coroutine = gh.get_github_readme_url(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == '404: Not Found'
    assert results['response_header'] is not None
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}/contents'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name


@pytest.mark.asyncio
async def test__get_github_readme_url__no_user_repo():
    # test with missing user_name
    user_name = None
    repo_name = 'existant'
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_readme_url(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == 'missing user/repo'
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}/contents'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name

    # test with empty user_name
    user_name = ''
    repo_name = 'existant'
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_readme_url(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == 'missing user/repo'
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}/contents'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name

    # test with missing repo_name
    user_name = 'non'
    repo_name = None
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_readme_url(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == 'missing user/repo'
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}/contents'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name

    # test with empty repo_name
    user_name = 'non'
    repo_name = ''
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_readme_url(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == 'missing user/repo'
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}/contents'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name

    # test with missing user_name and repo_name
    user_name = None
    repo_name = None
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_readme_url(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert results['error'] == 'missing user/repo'
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}/contents'
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name


@pytest.mark.asyncio
async def test__get_github_readme_url(github_token):
    user_name = 'apache'
    repo_name = 'airflow'

    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {github_token}'}) as session:  # noqa
        coroutine = gh.get_github_readme_url(
            user_name=user_name,
            repo_name=repo_name,
            session=session
        )
        results = await coroutine

    assert {'error', 'user_name', 'repo_name', 'url', 'readme_url', 'response_header'} == set(results.keys())  # noqa
    error_value = results.pop('error')
    assert error_value is None
    assert 'error' not in results.keys()
    assert all([x is not None for x in results.values()])
    assert results['user_name'] == user_name
    assert results['repo_name'] == repo_name
    assert results['url'] == f'https://api.github.com/repos/{user_name}/{repo_name}/contents'
    readme_url = results['readme_url']
    assert 'https://raw.githubusercontent.com/apache/airflow/main/README' in readme_url

    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {github_token}'}) as session:  # noqa
        coroutine = gh.get_github_readme_contents(
            url=readme_url,
            session=session,
        )
        results = await coroutine

    assert {'error', 'url', 'readme', 'response_header'} == set(results.keys())
    error_value = results.pop('error')
    assert error_value is None
    assert 'error' not in results.keys()
    assert all([x is not None for x in results.values()])
    assert results['url'] == readme_url
    assert isinstance(results['readme'], str)
    assert 'Airflow' in results['readme']


@pytest.mark.asyncio
async def test__get_github_readme_url__no_url():
    async with aiohttp.ClientSession() as session:
        coroutine = gh.get_github_readme_contents(
            url='',
            session=session,
        )
        results = await coroutine
        assert results == dict(error='missing url', url='')


@pytest.mark.asyncio
async def test__run_async__get_github_repo_info(github_token):
    arguments = [
        dict(user_name='apache', repo_name='airflow'),
        dict(user_name='dask', repo_name='dask'),
    ]
    results = await gh.run_async(
        func=gh.get_github_metadata,
        param_kwargs=arguments,
        token=github_token,
    )
    assert isinstance(results, list)
    assert all([x['error'] is None for x in results])
    user_names = [x['user_name'] for x in arguments]
    repo_names = [x['repo_name'] for x in arguments]
    assert len(results) == len(user_names)
    assert [x['user_name'] for x in results] == user_names
    assert [x['repo_name'] for x in results] == repo_names
    assert all([x['stargazers_count'] > 0 for x in results])



@pytest.mark.asyncio
async def test__run_async__get_github_readme_url(github_token):
    arguments = [
        dict(user_name='apache', repo_name='airflow'),
        dict(user_name='dask', repo_name='dask'),
    ]
    url_results = await gh.run_async(
        func=gh.get_github_readme_url,
        param_kwargs=arguments,
        token=github_token,
    )
    assert isinstance(url_results, list)
    assert all([x['error'] is None for x in url_results])
    user_names = [x['user_name'] for x in arguments]
    repo_names = [x['repo_name'] for x in arguments]
    assert len(url_results) == len(user_names)
    assert [x['user_name'] for x in url_results] == user_names
    assert [x['repo_name'] for x in url_results] == repo_names
    assert all([x['readme_url'] is not None for x in url_results])

    arguments = [dict(url=x['readme_url']) for x in url_results]
    content_results = await gh.run_async(
        func=gh.get_github_readme_contents,
        param_kwargs=arguments,
        token=github_token,
    )
    assert isinstance(content_results, list)
    assert all([x['error'] is None for x in content_results])
    assert [x['url'] for x in content_results] == [x['readme_url'] for x in url_results]
    assert all([x['readme'] is not None for x in content_results])
    assert all([x['readme'].strip() != '' for x in content_results])


def test__get_rate_limits(github_token):
    rates = gh.get_rate_limits(token=github_token)
    assert rates['limit'] == 5000
    assert rates['remaining'] >= 0 and rates['remaining'] <= 5000
    assert rates['reset_time'] is not None
