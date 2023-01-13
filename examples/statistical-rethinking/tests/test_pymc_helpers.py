import source.pymc_helpers as ph


def test__get_dataset_names(height_idata_prior, height_idata_posterior, height_idata_predictive):
    assert ph.get_dataset_names(height_idata_prior) == ['prior', 'prior_predictive', 'observed_data']  # noqa
    assert ph.get_dataset_names(height_idata_posterior) == ['posterior', 'sample_stats', 'observed_data']  # noqa
    assert ph.get_dataset_names(height_idata_predictive) == ['posterior_predictive', 'observed_data']  # noqa


def test__get_variable_names(
        height_idata_prior, height_idata_posterior, height_idata_predictive,
        height_expected_variables):

    assert set(ph.get_variable_names(height_idata_prior)) ==height_expected_variables  # noqa
    assert set(ph.get_variable_names(height_idata_prior, dataset_name='prior')) == height_expected_variables  # noqa
    assert ph.get_variable_names(height_idata_prior, dataset_name='prior_predictive') == ['height']
    assert ph.get_variable_names(height_idata_prior, dataset_name='observed_data') == ['height']

    assert set(ph.get_variable_names(height_idata_posterior)) == height_expected_variables
    assert set(ph.get_variable_names(height_idata_posterior, dataset_name='posterior')) == height_expected_variables  # noqa
    assert len(ph.get_variable_names(height_idata_posterior, dataset_name='sample_stats')) > 1
    assert ph.get_variable_names(height_idata_posterior, dataset_name='observed_data') == ['height']  # noqa

    assert ph.get_variable_names(height_idata_predictive) == ['height']
    assert ph.get_variable_names(height_idata_predictive, dataset_name='posterior_predictive') == ['height']  # noqa
    assert ph.get_variable_names(height_idata_predictive, dataset_name='observed_data') == ['height']  # noqa


def test__get_target_name(height_idata_prior, height_idata_posterior, height_idata_predictive):
    assert ph.get_target_name(height_idata_prior) == 'height'
    assert ph.get_target_name(height_idata_posterior) == 'height'
    assert ph.get_target_name(height_idata_predictive) == 'height'


def test__get_prior_samples(height_idata_prior, df_height, height_model_prior_samples):
    prior_samples_target = ph.get_prior_samples(height_idata_prior)
    assert prior_samples_target.shape == (len(df_height), height_model_prior_samples)
    abs(prior_samples_target.flatten().mean() - 178) < 5

    prior_samples_sigma = ph.get_prior_samples(height_idata_prior, variable_name='sigma')
    assert prior_samples_sigma.shape == (height_model_prior_samples,)
    assert abs(prior_samples_sigma.mean() - 25) < 5

    prior_samples_a = ph.get_prior_samples(height_idata_prior, variable_name='a')
    assert prior_samples_a.shape == (height_model_prior_samples,)
    assert abs(prior_samples_a.mean() - 178) < 5

    prior_samples_b = ph.get_prior_samples(height_idata_prior, variable_name='b')
    assert prior_samples_b.shape == (height_model_prior_samples,)
    assert abs(prior_samples_b.mean() - 0) < 3


def test__get_posterior_samples(
        height_idata_posterior, height_idata_predictive, df_height, height_model_posterior_samples,
        height_model_chains
        ):
    posterior_samples_target = ph.get_posterior_samples(height_idata_predictive)
    assert posterior_samples_target.shape == (len(df_height), height_model_posterior_samples * height_model_chains)  # noqa
    assert abs(posterior_samples_target.flatten().mean() - df_height['height'].mean()) < 5

    posterior_samples_sigma = ph.get_posterior_samples(height_idata_posterior, variable_name='sigma')  # noqa
    assert posterior_samples_sigma.shape == (height_model_posterior_samples * height_model_chains,)
    assert abs(posterior_samples_sigma.mean() - 10) < 5

    posterior_samples_a = ph.get_posterior_samples(height_idata_posterior, variable_name='a')
    assert posterior_samples_a.shape == (height_model_posterior_samples * height_model_chains,)
    assert abs(posterior_samples_a.mean() - 138) < 5

    posterior_samples_b = ph.get_posterior_samples(height_idata_posterior, variable_name='b')
    assert posterior_samples_b.shape == (height_model_posterior_samples * height_model_chains,)
    assert abs(posterior_samples_b.mean() - 0.56) < 1
