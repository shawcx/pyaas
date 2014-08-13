#!/usr/bin/env python

import os
import zipfile

from distutils.core import setup

zf = zipfile.ZipFile(os.path.join('pyaas', 'skel.zip'), 'w')
for base,directories,filenames in os.walk('skel'):
    for filename in filenames:
        path = os.path.join(base, filename)
        zf.write(path, path[5:])
zf.close()

setup(
    name = 'pyaas',
    version = '0.3.6',
    author = 'Matthew Oertle',
    author_email = 'moertle@gmail.com',
    url = 'https://github.com/moertle/pyaas',
    license  = 'MIT',
    description = 'Python-as-a-Service is a set of utilities for quickly creating Tornado applications.',
    long_description = open('README.rst').read(),
    packages = [
        'pyaas',
        'pyaas.handlers',
        'pyaas.handlers.auth',
        'pyaas.handlers.ws',
        'pyaas.storage',
        'pyaas.storage.engines',
        ],
    package_data = {
        'pyaas': ['skel.zip']
        },
    install_requires = [
        "tornado >= 3.0",
        ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        ],
    zip_safe = False
)
