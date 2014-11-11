#!/usr/bin/env python

import sys
import os
import argparse
import zipfile
import shutil
import time


def replace_in_file(src, dst, **kwargs):
    with open(src) as r:
        with open(dst, 'w') as w:
            for line in r:
                w.write(replace_in_str(line, **kwargs))

def replace_in_str(str, **kwargs):
    for key, value in kwargs.iteritems():
        str = str.replace(key, value)
    return str

def replace_all(file, **kwargs):
    dst = replace_in_str(file, **kwargs)
    if os.path.isdir(file):
        if file != dst:
            shutil.move(file, dst)
            file = dst
        for f in os.listdir(file):
            replace_all(os.path.join(file, f), **kwargs)
    else:
        if file == dst:
            tmp = '%s.tmp.%d' % (file, time.time())
            shutil.move(file, tmp)
            file = tmp
        replace_in_file(file, dst, **kwargs)
        os.remove(file)


def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('--name', '-n',
        default='example', required=True,
        help='Name of the project to create')

    args = argparser.parse_args()

    parts = args.name.split(' ')
    camel_name = ''.join([(p[0].upper() + p[1:]) for p in parts])
    lower_name = ''.join(parts)
    dstdir = os.path.join(os.getcwd(), os.path.basename(lower_name))
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

    replace_all(dstdir, example=lower_name, Example=camel_name)


if '__main__' == __name__:
    main()
