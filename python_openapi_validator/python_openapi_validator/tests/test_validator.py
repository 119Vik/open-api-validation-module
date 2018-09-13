import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from .. import validator
from .. import exceptions


def _get_mock_path(path):
    return "python_openapi_validator.validator.{}".format(path)


class TestValidator(unittest.TestCase):

    @mock.patch(_get_mock_path("OpenAPIValidator._init_spec"))
    def test_validator_init(self, init_spec_mock):
        data_provider = mock.MagicMock()

        o_v = validator.OpenAPIValidator(
            spec_data_provider=data_provider)

        self.assertEqual(o_v._spec_data_provider, data_provider)
        init_spec_mock.assert_called_once_with()

    @mock.patch(_get_mock_path("OpenAPIValidator._init_spec"))
    def test_spec_dict_without_heder(self, init_spec_mock):
        data_provider = mock.MagicMock()
        test_data = {"A": "a"}
        data_provider.get_data.return_value = test_data
        test_output = {"definitions": dict(test_data)}

        o_v = validator.OpenAPIValidator(
            spec_data_provider=data_provider)

        self.assertEqual(o_v._spec_dict, test_output)

        data_provider.get_data.assert_called_once_with()

    @mock.patch(_get_mock_path("OpenAPIValidator._init_spec"))
    def test_spec_dict_with_header(self, init_spec_mock):
        data_provider = mock.MagicMock()
        test_data = {"definitions": {"A": "a"}}
        data_provider.get_data.return_value = test_data
        test_output = {"definitions": {"A": "a"}}

        o_v = validator.OpenAPIValidator(
            spec_data_provider=data_provider)

        self.assertEqual(o_v._spec_dict, test_output)

        data_provider.get_data.assert_called_once_with()

    @mock.patch(_get_mock_path("OpenAPIValidator._init_spec_dict"))
    @mock.patch(_get_mock_path("Spec"))
    @mock.patch(_get_mock_path("settings"))
    def test_init_spec(self, settings_mock, Spec_mock, _spec_dict_mock):
        data_provider = mock.MagicMock()

        o_v = validator.OpenAPIValidator(
            spec_data_provider=data_provider)

        Spec_mock.from_dict.assert_called_once_with(
            o_v._spec_dict,
            config=settings_mock.BRAVADO_CONFIG
        )
        self.assertEqual(o_v._spec, Spec_mock.from_dict.return_value)

    @mock.patch(_get_mock_path("OpenAPIValidator._init_spec"))
    @mock.patch(_get_mock_path("validate_object"))
    def test_validation(self, validate_object_mock, init_spec_mock):
        data_provider = mock.MagicMock()

        o_v = validator.OpenAPIValidator(
            spec_data_provider=data_provider)
        model_spec = mock.MagicMock()
        data_sample = mock.MagicMock()

        with mock.patch.object(o_v, "_spec") as _speck_mock:
            o_v._perform_validation(model_spec, data_sample)

            validate_object_mock.assert_called_once_with(
                _speck_mock,
                model_spec,
                data_sample
            )

    @mock.patch(_get_mock_path("OpenAPIValidator._init_spec"))
    @mock.patch(_get_mock_path("validate_object"))
    def test_validation_of_incorrect_data(self, validate_object_mock,
                                          init_spec_mock):
        data_provider = mock.MagicMock()

        o_v = validator.OpenAPIValidator(
            spec_data_provider=data_provider)
        model_spec = mock.MagicMock()
        data_sample = mock.MagicMock()
        validate_object_mock.side_effect = Exception("Nothing is valid")

        with self.assertRaises(exceptions.ValidationException):
            with mock.patch.object(o_v, "_spec") as _speck_mock:
                o_v._perform_validation(model_spec, data_sample)

                validate_object_mock.assert_called_once_with(
                    _speck_mock,
                    model_spec,
                    data_sample
                )

    @mock.patch(_get_mock_path("OpenAPIValidator._init_spec"))
    @mock.patch(_get_mock_path("OpenAPIValidator._perform_validation"))
    def test_validation_against_model(self, _perform_validation_mock,
                                      init_spec_mock):
        spec_data_provider = mock.MagicMock()
        sample_data_provider = mock.MagicMock()

        o_v = validator.OpenAPIValidator(
            spec_data_provider=spec_data_provider)

        model_name = "Model"
        model_spec = mock.MagicMock()
        _speck_mock = {
            'definitions': {
                model_name: model_spec
            }
        }
        with mock.patch.object(o_v, "_spec_dict", _speck_mock):
            o_v.perform_validation_against_model(model_name,
                                                 sample_data_provider)

            sample_data_provider.get_data.assert_called_once_with()
            _perform_validation_mock.assert_called_once_with(
                model_spec,
                sample_data_provider.get_data.return_value
            )

    @mock.patch(_get_mock_path("OpenAPIValidator._init_spec"))
    @mock.patch(_get_mock_path("OpenAPIValidator._perform_validation"))
    def test_validation_against_unknown_model(self, _perform_validation_mock,
                                              init_spec_mock):
        spec_data_provider = mock.MagicMock()
        sample_data_provider = mock.MagicMock()

        o_v = validator.OpenAPIValidator(
            spec_data_provider=spec_data_provider)

        model_name = "Model2"
        model_spec = mock.MagicMock()
        _speck_mock = {
            'definitions': {
                "Model1": model_spec
            }
        }
        with self.assertRaises(exceptions.WrongArguments):
            with mock.patch.object(o_v, "_spec_dict", _speck_mock):
                o_v.perform_validation_against_model(model_name,
                                                     sample_data_provider)
