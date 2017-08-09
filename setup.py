#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ast import literal_eval
from os.path import join
from setuptools import setup

def get_version(source=join('reiterable','__init__.py')):
    with open(source) as f:
        for line in f:
            if line.startswith('__version__'):
                return literal_eval(line.partition('=')[2].lstrip())
    raise ValueError("VERSION not found")

README = ''
with open('README.rst', 'r') as f:
    README = f.read()

setup(name = 'reiterable',
      version = get_version(),
      packages = ['reiterable'],
      description = 'Wraps any iterable into a multi-usage iterable',
      long_description = README,
      author='Pierre-Antoine Champin',
      license='LGPL v3',
      platforms='OS Independant',
      url='https://github.com/pchampin/py_reiterable',
      tests_require=['pytest'],
      setup_requires = ["pytest-runner"],
)
