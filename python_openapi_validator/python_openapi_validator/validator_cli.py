import argparse

from . import validator
from . import data_providers


# Arguments reader
parser = argparse.ArgumentParser()

parser.add_argument(
    "spec_file_path",
    type=str,
    help="Path to File with Open API model definitions"
)

parser.add_argument(
    "test_file_path",
    type=str,
    help="Path to File with Data to be validated"
)

parser.add_argument(
    "model_name",
    type=str,
    help="Model that data sample should be validated against of"
)

args = parser.parse_args()


def main():
    full_spec_provider = data_providers.JSONDataProvider(
        file_path=args.spec_file_path)
    date_sample_provider = data_providers.JSONDataProvider(
        file_path=args.test_file_path)

    open_api_validator = validator.OpenAPIValidator(
        spec_data_provider=full_spec_provider
    )

    open_api_validator.perform_validation_against_model(
        model_name=args.model_name,
        sample_data_provider=date_sample_provider
    )


if __name__ == "__main__":
    main()
