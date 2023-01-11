import pandas as pd
import numpy as np
import pymc as pm

import source.pymc_helpers as ph


def test_asdf():
    df = pd.read_csv("/code/data/Howell1.csv", sep=";", header=0)

    num_prior_samples = 10
    num_posterior_samples = 1000
    num_chains = 3

    with pm.Model() as model:
        a = pm.Normal('a', mu=178, sigma=20)
        b = pm.Normal('b', mu=0, sigma=1)
        sigma = pm.Uniform('sigma', 0, 50)
        mu = a + np.exp(b) * (df.weight.values - df.weight.mean())
        height = pm.Normal('height', mu=mu, sigma=sigma, observed=df.height.values)  # noqa
        idata_prior = pm.sample_prior_predictive(samples=num_prior_samples, random_seed=42)

    with model:
        idata_posterior = pm.sample(draws=num_posterior_samples, tune=1000, chains=num_chains)
        idata_predictive = pm.sample_posterior_predictive(idata_posterior, random_seed=42)

    assert ph.get_dataset_names(idata_prior) == ['prior', 'prior_predictive', 'observed_data']
    assert ph.get_dataset_names(idata_posterior) == ['posterior', 'sample_stats', 'observed_data']
    assert ph.get_dataset_names(idata_predictive) == ['posterior_predictive', 'observed_data']

    expected_variables = {'sigma', 'b', 'a'}
    assert set(ph.get_variable_names(idata_prior)) == expected_variables
    assert set(ph.get_variable_names(idata_prior, dataset_name='prior')) == expected_variables
    assert ph.get_variable_names(idata_prior, dataset_name='prior_predictive') == ['height']
    assert ph.get_variable_names(idata_prior, dataset_name='observed_data') == ['height']

    assert set(ph.get_variable_names(idata_posterior)) == expected_variables
    assert set(ph.get_variable_names(idata_posterior, dataset_name='posterior')) == expected_variables  # noqa
    assert len(ph.get_variable_names(idata_posterior, dataset_name='sample_stats')) > 1
    assert ph.get_variable_names(idata_posterior, dataset_name='observed_data') == ['height']

    assert ph.get_variable_names(idata_predictive) == ['height']
    assert ph.get_variable_names(idata_predictive, dataset_name='posterior_predictive') == ['height']  # noqa
    assert ph.get_variable_names(idata_predictive, dataset_name='observed_data') == ['height']

    assert ph.get_target_name(idata_prior) == 'height'
    assert ph.get_target_name(idata_posterior) == 'height'
    assert ph.get_target_name(idata_predictive) == 'height'

    prior_samples_target = ph.get_prior_samples(idata_prior)
    assert prior_samples_target.shape == (len(df), num_prior_samples)
    abs(prior_samples_target.flatten().mean() - 178) < 5

    prior_samples_sigma = ph.get_prior_samples(idata_prior, variable_name='sigma')
    assert prior_samples_sigma.shape == (num_prior_samples,)
    assert abs(prior_samples_sigma.mean() - 25) < 5

    prior_samples_a = ph.get_prior_samples(idata_prior, variable_name='a')
    assert prior_samples_a.shape == (num_prior_samples,)
    assert abs(prior_samples_a.mean() - 178) < 5

    prior_samples_b = ph.get_prior_samples(idata_prior, variable_name='b')
    assert prior_samples_b.shape == (num_prior_samples,)
    assert abs(prior_samples_b.mean() - 0) < 3

    posterior_samples_target = ph.get_posterior_samples(idata_predictive)
    assert posterior_samples_target.shape == (len(df), num_posterior_samples * num_chains)
    assert abs(posterior_samples_target.flatten().mean() - df['height'].mean()) < 5

    posterior_samples_sigma = ph.get_posterior_samples(idata_posterior, variable_name='sigma')
    assert posterior_samples_sigma.shape == (num_posterior_samples * num_chains,)
    assert abs(posterior_samples_sigma.mean() - 10) < 5

    posterior_samples_a = ph.get_posterior_samples(idata_posterior, variable_name='a')
    assert posterior_samples_a.shape == (num_posterior_samples * num_chains,)
    assert abs(posterior_samples_a.mean() - 138) < 5

    posterior_samples_b = ph.get_posterior_samples(idata_posterior, variable_name='b')
    assert posterior_samples_b.shape == (num_posterior_samples * num_chains,)
    assert abs(posterior_samples_b.mean() - 0.56) < 1
