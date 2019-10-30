#!/usr/bin/env python

from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '0.1'

setup(
    name='s3data',
    version=version,
    install_requires=requirements,
    python_requires='>=3',
    author='Brian Cantoni',
    author_email='brian@cantoni.org',
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    url='https://github.com/bcantoni/s3data/',
    license='MIT',
    description='Simple persistent data storage in AWS S3',
    long_description=long_description,
)
