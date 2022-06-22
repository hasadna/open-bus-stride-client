from setuptools import setup, find_packages
from os import path
import time

if path.exists("VERSION.txt"):
    # this file can be written by CI tools (e.g. Travis)
    with open("VERSION.txt") as version_file:
        version = version_file.read().strip().strip("v")
else:
    version = str(time.time())


extras_cli = ['click==8.1.3']


setup(
    name='open-bus-stride-client',
    version=version,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['requests', 'pytz', 'json-stream==1.3.0'],
        'all': [
            *extras_cli,
        ]
    },
    entry_points={
        'console_scripts': [
            'stride = stride.cli:main',
        ]
    },
)
