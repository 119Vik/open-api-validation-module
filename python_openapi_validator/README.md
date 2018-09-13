## Description
Python OpenAPI Validator is thin wrapper on top of `bravado_core`. It helps quickly test your data against known schema defined according to OpenAPI standard.  

## Local testing 
Prepare Docker Image 

`docker build -t python_openapi_validator .`

Run Test host for file validation

`docker run -p 2222:22 -d python_openapi_validator`

SSH to container with password `root:root` 

`ssh root@0.0.0.0 -p 2222`

