#!/usr/bin/env python

import os

from distutils.core import setup

import pyaas.skel

setup(
    name='example',
    author='Your Name Here',
    author_email='your@email',
    long_description=open('README.rst').read(),
    version='0.1',
    description='Example Project',
    license='TBD',
    packages=[
        'example',
        'example.handlers',
    ],
    scripts=[
        'bin/example.py',
    ],
    data_files=pyaas.skel.add_data_files('etc', 'share', 'var'),
    install_requires=[
        'pyaas >= 0.5.3',
    ],
    zip_safe=False
)
