from typing import Callable, Optional
import pymc as pm
import pandas as pd
import numpy as np
import arviz as az


def get_dataset_names(inference_data: az.InferenceData) -> list[str]:
    """
    Returns the dataset names associated with `inference_data`

    Args:
        inference_data:
            object returned from e.g. `pm.sample_prior_predictive()`, `pm.sample()`, or
            `pm.sample_posterior_predictive()`
    """
    return inference_data._group_names(None, None)


def get_variable_names(
        inference_data: az.InferenceData,
        dataset_name: Optional[str] = None) -> list[str]:
    """
    Returns the variable names associated with a dataset in `inference_data`.

    Args:
        inference_data:
            object returned from e.g. `pm.sample_prior_predictive()`, `pm.sample()`, or
            `pm.sample_posterior_predictive()`
        dataset_name:
            The name of the dataset to get the variable names from. If `None`, the first dataset
            returned from `get_dataset_names()` is used.
    """
    if dataset_name is None:
        dataset_name = get_dataset_names(inference_data)[0]

    return list(inference_data[dataset_name].data_vars)


def get_target_name(inference_data: az.InferenceData) -> str:
    """
    Returns the name of the target variable associated with `inference_data`.

    Args:
        inference_data:
            object returned from e.g. `pm.sample_prior_predictive()`, `pm.sample()`, or
            `pm.sample_posterior_predictive()`
    """
    return get_variable_names(inference_data=inference_data, dataset_name='observed_data')[0]


def get_prior_samples(
        inference_data: az.InferenceData,
        variable_name: Optional[str] = None) -> np.ndarray:
    """
    Returns a 1d or 2d array of samples associated with the prior distributions.

    If `variable_name` is None, then the samples returned correspond to the target variable. In
    this case, a 2d array is returned and the number of rows corresponds to the number of
    observations given to the model. The number of columns corresponds to the value passed into the
    `samples` parameter of the `pm.sample_prior_predictive` function.

    If `variable_name` is not None, then the samples returned correspond to the model parameter
    with the same name. In this case, a 1d array is returned and the length corresponds to the
    value passed into the `samples` parameter of the `pm.sample_prior_predictive` function.

    args:
        inference_data: object returned by `pm.sample_prior_predictive`
        variable_name:
            if None, returns the samples associated with the target variable
            otherwise, returns the samples associated with the model parameter passed in
    """
    if variable_name is None:
        variable_name = get_target_name(inference_data)
        dataset_name = 'prior_predictive'
    else:
        dataset_name = 'prior'

    samples = inference_data[dataset_name][variable_name].\
        stack(sample=['chain', 'draw']).\
        data
    return samples


def get_posterior_samples(
        inference_data: az.InferenceData,
        variable_name: Optional[str] = None) -> np.ndarray:
    """
    Returns a 1d or 2d array of samples associated with the posterior distributions.

    If `variable_name` is None, then the samples returned correspond to the target variable. In
    this case, a 2d array is returned and the number of rows corresponds to the number of
    observations given to the model. The number of columns corresponds to the number of `draws`
    multiplied by the number of `chains` specified in `pm.sample()`.

    If `variable_name` is not None, then the samples returned correspond to the model parameter
    with the same name. In this case, a 1d array is returned and the length corresponds to the
    number of `draws` multiplied by the number of `chains` specified in `pm.sample()`.

    args:
        inference_data:
            object returned by `pm.sample_posterior_predictive`
            For samples associated with target variable, pass the object returned by the
            `pm.sample_posterior_predictive` function.
            For samples associated with one of the model variables, pass the object returned by the
            `pm.sample` function.

        variable_name:
            if None, returns the samples associated with the target variable
            otherwise, returns the samples associated with the model parameter passed in
    """
    if variable_name is None:
        variable_name = get_target_name(inference_data)
        dataset_name = 'posterior_predictive'
    else:
        dataset_name = 'posterior'

    samples = inference_data[dataset_name][variable_name].\
        stack(sample=['chain', 'draw']).\
        data
    return samples


def posterior_predict_inference(
        model: pm.model.Model,
        idata_posterior: az.InferenceData,
        data: pd.DataFrame,
        x_name: str = 'X',
        y_name: str = 'y') -> az.InferenceData:
    """
    Makes predictions on out of sample data via `set_data()` function and returns the corresponding
    az.InferenceData object.

    When defining the model, you must explicitly specify the X and y data used by the model, so
    that data can be swapped out with an out of sample dataset. For example, with the `X` and `y`
    variables used in the following example:

    ```
    X = pm.MutableData("X", df_height.weight.values)
    y = pm.MutableData("y", df_height.height.values)

    a = pm.Normal('a', mu=178, sigma=20)
    b = pm.Normal('b', mu=0, sigma=1)
    sigma = pm.Uniform('sigma', 0, 50)
    mu = a + np.exp(b) * (X - df_height.weight.mean())
    height = pm.Normal('height', mu=mu, sigma=sigma, observed=y)
    ```

    Args:
        model:
            the PYMC model to use
        inference_data:
            object returned by `pm.sample()`
        data:
            the new data to make predictions with
        x_name:
            the name of the X and y data. In the example above, the name of the X dataset is "X".
        y_name:
            the name of the X and y data. In the example above, the name of the y dataset is "y".
    """
    # Update data reference.
    pm.set_data({x_name: data, y_name: np.zeros(len(data))}, model=model)
    # Generate posterior samples.
    return pm.sample_posterior_predictive(idata_posterior, model=model)


def posterior_predict(
        model: pm.model.Model,
        idata_posterior: az.InferenceData,
        data: pd.DataFrame,
        x_name: str = 'X',
        y_name: str = 'y') -> np.ndarray:
    """
    Makes predictions on out of sample data via `set_data()` function and returns the samples
    in a np.ndarray with a length equal to the length of the new dataset `data` and the number of
    columns equal to the number draws multiplied by the number of chains passed to `pm.sample()`.

    When defining the model, you must explicitly specify the X and y data used by the model, so
    that data can be swapped out with an out of sample dataset. For example, with the `X` and `y`
    variables used in the following example:

    ```
    X = pm.MutableData("X", df_height.weight.values)
    y = pm.MutableData("y", df_height.height.values)

    a = pm.Normal('a', mu=178, sigma=20)
    b = pm.Normal('b', mu=0, sigma=1)
    sigma = pm.Uniform('sigma', 0, 50)
    mu = a + np.exp(b) * (X - df_height.weight.mean())
    height = pm.Normal('height', mu=mu, sigma=sigma, observed=y)
    ```

    Args:
        model:
            the PYMC model to use
        inference_data:
            object returned by `pm.sample()`
        data:
            the new data to make predictions with
        x_name:
            the name of the X and y data. In the example above, the name of the X dataset is "X".
        y_name:
            the name of the X and y data. In the example above, the name of the y dataset is "y".
    """
    idata = posterior_predict_inference(
        model=model,
        idata_posterior=idata_posterior,
        data=data,
        x_name=x_name,
        y_name=y_name,
    )
    samples = idata['posterior_predictive'][get_target_name(idata)]\
        .stack(sample=['chain', 'draw']).\
        data
    return samples


def predict(
        model: pm.model.Model,
        idata_posterior: az.InferenceData,
        data: pd.DataFrame,
        aggregation_func: Callable = np.median,
        x_name: str = 'X',
        y_name: str = 'y') -> float:
    """
    Makes predictions on out of sample data via `set_data()` function and returns the samples
    in a np.ndarray with a length equal to the length of the new dataset `data` and the number of
    columns equal to the number draws multiplied by the number of chains passed to `pm.sample()`.

    When defining the model, you must explicitly specify the X and y data used by the model, so
    that data can be swapped out with an out of sample dataset. For example, with the `X` and `y`
    variables used in the following example:

    ```
    X = pm.MutableData("X", df_height.weight.values)
    y = pm.MutableData("y", df_height.height.values)

    a = pm.Normal('a', mu=178, sigma=20)
    b = pm.Normal('b', mu=0, sigma=1)
    sigma = pm.Uniform('sigma', 0, 50)
    mu = a + np.exp(b) * (X - df_height.weight.mean())
    height = pm.Normal('height', mu=mu, sigma=sigma, observed=y)
    ```

    Args:
        model:
            the PYMC model to use
        inference_data:
            object returned by `pm.sample()`
        data:
            the new data to make predictions with
        aggregation_func:
            the method that will aggregate all of the samples for each new observation/row in
            `data`
        x_name:
            the name of the X and y data. In the example above, the name of the X dataset is "X".
        y_name:
            the name of the X and y data. In the example above, the name of the y dataset is "y".
    """
    # predict a point estimate
    samples = posterior_predict(
        model=model,
        idata_posterior=idata_posterior,
        data=data,
        x_name=x_name,
        y_name=y_name,
    )
    return aggregation_func(samples, axis=1)
