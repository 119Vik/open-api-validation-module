from setuptools import setup

setup(name="python_openapi_validator",
      version="0.1",
      description=("Wrapper on top of bravado_core that helps validate data"
                   " samples against OpenApi Model definition"),
      author='Vitalii Kostenko',
      author_email='vitalij.kostenko@gmail.com',
      license='LGPL-3.0',
      packages=['python_openapi_validator'],
      zip_safe=False,
      install_requires=[
          'bravado_core',
      ],
      entry_points={
        'console_scripts': [
            'validate_sample=python_openapi_validator.validator_cli:main',
        ]
      })
