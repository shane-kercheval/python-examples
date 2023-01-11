from typing import Optional
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
        variable_name = get_target_name(inference_data)
    samples = inference_data['prior_predictive'][variable_name].\
        stack(sample=['chain', 'draw']).\
        data
    return samples



def get_posterior_samples(posterior_inference: az.InferenceData, variable_name: str):
    return posterior_inference.posterior[variable_name].stack(sample=["chain", "draw"]).data


# def get_prediction_samples(prediction_inference: az.InferenceData):
#     variable_name = get_variable_names(prediction_inference)[0]
#     return prediction_inference.posterior_predictive[variable_name].stack(sample=["chain", "draw"]).data


def get_prediction_samples(prediction_inference: az.InferenceData, type: str = 'posterior'):
    """
    Args:
        type:
            a string with a value of either `posterior` or `prior`
    """
    variable_name = get_variable_names(prediction_inference)[0]
    return prediction_inference[f'{type}_predictive'][variable_name].stack(sample=["chain", "draw"]).data
