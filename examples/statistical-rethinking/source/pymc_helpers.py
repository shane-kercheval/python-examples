from typing import Optional
import numpy as np
import arviz as az


def get_dataset_names(inference_data: az.InferenceData) -> list[str]:
    return inference_data._group_names(None, None)


def get_variable_names(
        inference_data: az.InferenceData,
        dataset_name: Optional[str] = None) -> list[str]:

    if dataset_name is None:
        dataset_name = get_dataset_names(inference_data)[0]

    return list(inference_data[dataset_name].data_vars)


def get_target_name(inference_data: az.InferenceData) -> str:
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
    with the same name. In this case, a 1d array is returned and the length corresponds to the number of `draws`
    multiplied by the number of `chains` specified in `pm.sample()`.

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
