## Usage example

Build container 

`docker build -t python_openapi_validator python_openapi_validator/`

Run container

`docker run -p 2222:22 -d python_openapi_validator`

Run data validation

`ansible-playbook -i ansible_inventory validate.yaml 
    --ask-pass 
    --extra-vars='target=localhost spec_file_path=test_data/validation_rules.schema  test_file_path=test_data/valid_sample.json model_name=TestModel' 
    -e ansible_ssh_port=2222`