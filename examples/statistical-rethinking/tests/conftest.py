import pytest
import pandas as pd
import numpy as np
import pymc as pm


@pytest.fixture(scope="session")
def df_height():
    return pd.read_csv("/code/data/Howell1.csv", sep=";", header=0)


@pytest.fixture(scope="session")
def height_model_prior_samples():
    return 10


@pytest.fixture(scope="session")
def height_model_posterior_samples():
    return 1000


@pytest.fixture(scope="session")
def height_model_chains():
    return 3


@pytest.fixture(scope="session")
def height_expected_variables():
    return {'sigma', 'b', 'a'}


@pytest.fixture(scope="session")
def height_model(df_height):
    with pm.Model() as model:
        a = pm.Normal('a', mu=178, sigma=20)
        b = pm.Normal('b', mu=0, sigma=1)
        sigma = pm.Uniform('sigma', 0, 50)
        mu = a + np.exp(b) * (df_height.weight.values - df_height.weight.mean())
        height = pm.Normal('height', mu=mu, sigma=sigma, observed=df_height.height.values)  # noqa

    return model


@pytest.fixture(scope="session")
def height_idata_prior(height_model, height_model_prior_samples):
    with height_model:
        return pm.sample_prior_predictive(samples=height_model_prior_samples, random_seed=42)


@pytest.fixture(scope="session")
def height_idata_posterior(height_model, height_model_posterior_samples, height_model_chains):
    with height_model:
        return pm.sample(
            draws=height_model_posterior_samples,
            chains=height_model_chains,
            random_seed=42
        )


@pytest.fixture(scope="session")
def height_idata_predictive(height_model, height_idata_posterior):
    with height_model:
        return pm.sample_posterior_predictive(height_idata_posterior, random_seed=42)
