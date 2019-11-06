from os import environ
from setuptools import setup, find_packages

from exceptions import EnvironmentUnsetError

required_env_vars = [
    'WFB_PROJECT_NAME',
    'WFB_FLASK_SECRET_KEY'
]
for var in required_env_vars:
    if var not in environ:
        raise EnvironmentUnsetError(var)

optional_setup = {}
if 'WFB_AUTHOR_NAME' in environ:
    optional_setup['author'] = environ['WFB_AUTHOR_NAME']
if 'WFB_AUTHOR_EMAIL' in environ:
    optional_setup['author_email'] = environ['WFB_AUTHOR_EMAIL']
if 'WFB_AUTHOR_NAME' in environ:
    optional_setup['url'] = environ['WFB_PROJECT_URL']

setup(
    name=environ['WFB_PROJECT_NAME'],
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'datetime',
        'Flask',
        'Flask-SQLAlchemy',
        'mysql-connector-python',
        'WTForms'
    ],
    **optional_setup
)
