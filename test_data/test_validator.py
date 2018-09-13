import json
from bravado_core.spec import Spec
from bravado_core.validate import validate_object


def perform_validation(full_spec, model_spec, sample_file_name):
    with open(sample_file_name, 'r') as data_file:
        data_dict = json.load(data_file)

    try:
        validate_object(full_spec, model_spec, data_dict)
    except Exception as e:
        print("Data sample is invalid./n", e)
    else:
        print("Data sample is valid.")


if __name__ == "__main__":
    spec_file_name = "validation_rules.schema"
    bravado_config = {
        'validate_swagger_spec': False,
        'validate_requests': False,
        'validate_responses': False,
        'use_models': True,
    }

    with open(spec_file_name, 'r') as spec_file:
        spec_dict = json.load(spec_file)

    if "definitions" not in spec_dict:
        spec_dict = {
            "definitions": spec_dict
        }

    spec = Spec.from_dict(spec_dict, config=bravado_config)
    TestModel = spec_dict['definitions']['TestModel']
    test_data_samples = [
        "valid_sample.json",
        "invalid_sample.json"
    ]
    for file_name in test_data_samples:
        perform_validation(
            full_spec=spec,
            model_spec=TestModel,
            sample_file_name=file_name)
