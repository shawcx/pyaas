#!/usr/bin/env python

import sys
import os

import tornado.template


def main():
    root = os.getcwd()
    root = os.path.abspath(root)

    template_directory = os.path.join(root, 'templates')

    loader = tornado.template.Loader(template_directory)

    trim = len(template_directory) + 1

    for (base,directories,filenames) in os.walk(template_directory):
        for filename in filenames:
            if not filename.endswith('.html'):
                continue
            path = os.path.join(base, filename)[trim:]
            content = loader.load(path).generate()

            dest = os.path.join(root, 'site', path)

            try:
                os.makedirs(os.path.dirname(dest))
            except OSError:
                pass

            open(dest, 'wb').write(content)

            print path, '=>', dest


if '__main__' == __name__:
    main()
