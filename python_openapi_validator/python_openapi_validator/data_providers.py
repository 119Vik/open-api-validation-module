import json

from . import exceptions


class BaseDataProvider(object):

    def get_data(self):
        raise NotImplementedError


class FileDataProvider(BaseDataProvider):

    def __init__(self, file_path):
        self._file_path = file_path


class JSONDataProvider(FileDataProvider):

    def get_data(self):
        try:
            with open(self._file_path, 'r') as data_file:
                data_dict = json.load(data_file)
        except FileNotFoundError:
            raise exceptions.WrongArguments(
                "file {} does not exists".format(self._file_path)
            )
        except json.decoder.JSONDecodeError:
            raise exceptions.WrongArguments(
                "file {} is not JSON".format(self._file_path)
            )

        return data_dict
