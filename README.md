## Usage example

Build container 

`docker build -t python_openapi_validator python_openapi_validator/`

Run container

`docker run -p 2222:22 -d python_openapi_validator`

Run data validation without special module

`ansible-playbook -i ansible_inventory raw_validate.yaml 
    --ask-pass 
    --extra-vars='target=localhost spec_file_path=test_data/validation_rules.schema  test_file_path=test_data/valid_sample.json model_name=TestModel' 
    -e ansible_ssh_port=2222`
     
Run data validation with special module that available at https://github.com/119Vik/ansible/tree/remote_data_validator

`ansible-playbook -i ansible_inventory validate_with_module.yaml 
    --ask-pass 
    --extra-vars='target=localhost spec_file_path=test_data/validation_rules.schema  test_file_path=test_data/valid_sample.json model_name=TestModel' 
    -e ansible_ssh_port=2222`