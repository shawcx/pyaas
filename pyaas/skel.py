#!/usr/bin/env python

import sys
import os
import argparse
import zipfile


def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('--name', '-n',
        default='example', required=True,
        help='Name of the project to create')

    args = argparser.parse_args()

    dstdir = os.path.join(os.getcwd(), os.path.basename(args.name))
    dstdir = os.path.abspath(dstdir)

    try:
        os.mkdir(dstdir)
    except OSError as e:
        if 17 == e.errno:
            sys.stderr.write('Directory with that name already exists.\n')
            sys.exit(-1)
        raise

    skel = os.path.dirname(__file__)
    skel = os.path.join(skel, 'skel.zip')
    skel = zipfile.ZipFile(skel, 'r')

    skel.extractall(dstdir)

    os.chdir(dstdir)

    for src in ['example.py', os.path.join('etc', 'example.ini')]:
        dst = src.replace('example', args.name)
        os.rename(src, dst)

if '__main__' == __name__:
    main()
