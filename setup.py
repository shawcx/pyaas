#!/usr/bin/env python

import os
import zipfile

from distutils.core import setup

zf = zipfile.ZipFile(os.path.join('pyaas', 'skel.zip'), 'w')

for base,directories,filenames in os.walk('skel'):
    for filename in filenames:
        path = os.path.join(base, filename)
        print path
        zf.write(path, path[5:])

zf.close()

print '*' * 80
print os.path.join('pyaas', 'skel.zip')

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
    package_data = {
        'pyaas': ['skel.zip']
        },
    url = 'https://github.com/moertle/pyaas',
    license  = 'MIT',
    description = 'Python-as-a-Service is a set of utilities for quickly creating Tornado applications.',
    long_description = open('README.md').read(),
    install_requires = [
        "tornado >= 3.0",
    ],
    zip_safe = True
)
