import json
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from .. import data_providers
from .. import exceptions


class TestBaseDataProvider(unittest.TestCase):

    def test_getting_data_from_provider(self):
        provider = data_providers.BaseDataProvider()
        with self.assertRaises(NotImplementedError):
            provider.get_data()


class TestFileDataProvider(unittest.TestCase):

    def setUp(self):
        self._test_path = "somepath"

    def test_init_data_from_provider(self):
        provider = data_providers.FileDataProvider(file_path=self._test_path)
        self.assertEqual(provider._file_path, self._test_path)

    def test_getting_data_from_provider(self):
        provider = data_providers.FileDataProvider(file_path=self._test_path)
        with self.assertRaises(NotImplementedError):
            provider.get_data()


class TestJSONDataProvider(unittest.TestCase):

    def setUp(self):
        self._test_path = "somepath"

    def test_init_data_from_provider(self):
        provider = data_providers.JSONDataProvider(file_path=self._test_path)
        self.assertEqual(provider._file_path, self._test_path)

    def test_getting_data_from_provider(self):
        mock_data = {
            "test": "test"
        }
        mock_file_content = json.dumps(mock_data)
        mock_path = "python_openapi_validator.data_providers.open"

        provider = data_providers.JSONDataProvider(file_path=self._test_path)
        context_mock = mock.MagicMock()
        context_mock.return_value.read.return_value = mock_file_content

        with mock.patch(mock_path) as mocked_open:
            mocked_open.return_value.__enter__ = context_mock
            result = provider.get_data()

        self.assertEqual(mock_data, result)

    def test_getting_data_from_fake_file(self):
        mock_path = "python_openapi_validator.data_providers.open"

        provider = data_providers.JSONDataProvider(file_path=self._test_path)

        with self.assertRaises(exceptions.WrongArguments):
            with mock.patch(mock_path) as mocked_open:
                mocked_open.side_effect = IOError
                provider.get_data()

    def test_getting_data_from_non_json_file(self):
        mock_file_content = "abw"
        mock_path = "python_openapi_validator.data_providers.open"

        provider = data_providers.JSONDataProvider(file_path=self._test_path)
        context_mock = mock.MagicMock()
        context_mock.return_value.read.return_value = mock_file_content

        with self.assertRaises(exceptions.WrongArguments):
            with mock.patch(mock_path) as mocked_open:
                mocked_open.return_value.__enter__ = context_mock
                provider.get_data()
