from setuptools import setup, find_packages
from os import path
import time


if path.exists("VERSION.txt"):
    # this file can be written by CI tools (e.g. Travis)
    with open("VERSION.txt") as version_file:
        version = version_file.read().strip().strip("v")
else:
    version = str(time.time())


extras_cli = ['click>=7.0']
extras_jupyter = ['jupyterlab', 'ipywidgets']
extras_notebooks = ['pandas>=1.3,<1.4']
extras_urbanaccess = ['urbanaccess==0.2.2', 'geopandas==0.10.2']
extras_apiproxy = ['psutil']


setup(
    name='open-bus-stride-client',
    version=version,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    install_requires=['requests', 'pytz', 'json-stream==1.3.0'],
    extras_require={
        'cli': extras_cli,
        'notebooks': extras_notebooks,
        'urbanaccess': extras_urbanaccess,
        'apiproxy': extras_apiproxy,
        'all': [
            *extras_cli,
            *extras_jupyter,
            *extras_notebooks,
            *extras_urbanaccess,
            *extras_apiproxy,
        ]
    },
    entry_points={
        'console_scripts': [
            'stride = stride.cli:main',
        ]
    },
)
