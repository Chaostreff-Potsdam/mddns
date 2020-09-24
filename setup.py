#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='mddns',
    version='0.1',
    description = 'Another Webfrontend and API to PowerDNS with a clear user-to-recordname centered design.',
    license='MIT',
    author='Sven Koehler',
    author_email='sven.koehler@hpi.de',
    install_requires=[
        "django",
        "requests",
        ],
    packages=find_packages()
)
