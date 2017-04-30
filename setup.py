#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# use requirements.txt for dependencies
with open('requirements.txt') as f:
    required = map(lambda s: s.strip(), f.readlines())

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='manifold_note',
    version='0.1.0',
    description='A CRUD system to add store notes in a file-storage',
    long_description=readme,
    install_requires=required,
    author='Kartik Prabhu',
    author_email='me@kartikprabhu.com',
    url='https://github.com/kartikprabhu/manifold_note',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
