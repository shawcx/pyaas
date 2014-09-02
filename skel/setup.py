#!/usr/bin/env python

import os

from distutils.core import setup


def add_data_files(*include_dirs):
    data_files = []
    for include_dir in include_dirs:
        for root, directories, filenames in os.walk(include_dir):
            include_files = []
            for filename in filenames:
                include_files.append(os.path.join(root, filename))
            if include_files:
                data_files.append((root, include_files))
    return data_files


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
    data_files=add_data_files('etc', 'share'),
    install_requires=[
        'pyaas >= 0.3.9',
    ],
    zip_safe=False
)
