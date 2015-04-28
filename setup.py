"""
Weatherpy Setup
"""
from setuptools import setup

import weatherpy

setup(
    name='weatherpy',
    version=weatherpy.__version__,
    description=('Command line utility to display formatted weather info from'
                 'Weather Underground'),
    author='Jack Wink',
    author_email='jackwink@umich.edu',
    license='MIT',
    packages=['weatherpy'],
    install_requires=['requests>=2.0.0'],
    tests_require=['coverage', 'nose'],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'weatherpy = weatherpy:main',
        ]
    },
)
