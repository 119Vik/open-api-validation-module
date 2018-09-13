from bravado_core.spec import Spec
from bravado_core.validate import validate_object

from . import settings
from . import exceptions


class OpenAPIValidator(object):

    """Open API validator class."""

    def __init__(self, spec_data_provider):
        self._spec = None

        self._spec_data_provider = spec_data_provider

        self._init_spec()

    @property
    def _spec_dict(self):
        """
        Get Full definition of models specifications from any suitable source.

        This implementation get's full specification from file.
        """
        spec_dict = self._spec_data_provider.get_data()

        if "definitions" not in spec_dict:
            spec_dict = {
                "definitions": spec_dict
            }
        return spec_dict

    def _init_spec(self):
        """Initialise API specification object."""
        self._spec = Spec.from_dict(
            self._spec_dict,
            config=settings.BRAVADO_CONFIG
        )

    def _perform_validation(self, model_spec, data_sample):
        try:
            validate_object(self._spec, model_spec, data_sample)
        except Exception as e:
            raise exceptions.ValidationException(str(e))

    def perform_validation_against_model(self, model_name,
                                         sample_data_provider):
        try:
            model_spec = self._spec['definitions'][model_name]
        except KeyError:
            raise exceptions.WrongArguments("Requested model is not in spec")

        data_sample = sample_data_provider.get_data()

        self._perform_validation(model_spec, data_sample)
