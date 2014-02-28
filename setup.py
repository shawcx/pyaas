#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'pyaas',
    version = '0.1.2',
    author = 'Matthew Oertle',
    author_email = 'moertle@gmail.com',
    packages = [
        'pyaas',
        'pyaas.handlers',
        'pyaas.handlers.auth',
        'pyaas.handlers.ws',
        ],
    url = 'https://github.com/moertle/pyaas',
    license  = 'MIT',
    description = 'Python-as-a-Service is a set of utilities for creating Tornado applications.',
    long_description = open('README.md').read(),
    install_requires = [
        "tornado >= 3.0",
    ],
    zip_safe = True
)
