import pandas as pd
import numpy as np
import pymc as pm

import source.pymc_helpers as ph


def test_asdf():
    df = pd.read_csv("/code/data/Howell1.csv", sep=";", header=0)

    num_prior_samples = 10

    with pm.Model() as model:
        a = pm.Normal('a', mu=178, sigma=20)
        b = pm.Normal('b', mu=0, sigma=1)
        sigma = pm.Uniform('sigma', 0, 50)
        mu = a + np.exp(b) * (df.weight.values - df.weight.mean())
        height = pm.Normal('height', mu=mu, sigma=sigma, observed=df.height.values)  # noqa
        idata_prior = pm.sample_prior_predictive(samples=num_prior_samples, random_seed=42)

    with model:
        idata_posterior = pm.sample(draws=100, tune=10, chains=3)
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


    len(df)

    from typing import Optional
    import arviz as az
    def get_prior_samples(
            inference_data: az.InferenceData,
            variable_name: Optional[str] = None) -> np.ndarray:
        """
        Returns a 2d array of samples associated with the prior distributions.

        The number of rows in the 2d array corresponds to the number of observations given to the
        model. The number of columns corresponds to the value passed into the `samples` parameter
        of the `pm.sample_prior_predictive` function.

        args:
            inference_data: object returned by `pm.sample_prior_predictive`
            variable_name:
                if None, returns the samples associated with the target variable
                otherwise, returns the samples associated with the variable passed in
        """
        if variable_name is None:
            variable_name = ph.get_target_name(inference_data)
        samples = inference_data['prior_predictive'][variable_name].\
            stack(sample=['chain', 'draw']).\
            data
        return samples

    prior_samples = get_prior_samples(idata_prior)
    assert prior_samples.shape == (len(df), num_prior_samples)





    len(prior_samples.flatten())



    prior_samples.prior_predictive["height"].data[0].flatten()


    ph.get_variable_names(idata_prior, dataset_name='observed')

    ph.get_dataset_names(idata_posterior)
    ph.get_dataset_names(idata_predictive)
