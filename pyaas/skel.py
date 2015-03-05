#!/usr/bin/env python

import sys
import os
import argparse
import zipfile
import shutil
import time


def add_data_files(*include_dirs):
    'called from setup.py in skeleton projects'
    data_files = []
    for include_dir in include_dirs:
        for root, directories, filenames in os.walk(include_dir):
            include_files = []
            for filename in filenames:
                # do not bring along certain files
                if filename.endswith('.local'):
                    continue
                include_files.append(os.path.join(root, filename))
            if include_files:
                data_files.append((root, include_files))
    return data_files


def replace_in_file(src, dst, **kwargs):
    with open(src) as r:
        with open(dst, 'w') as w:
            for line in r:
                w.write(replace_in_string(line, **kwargs))


def replace_in_string(string, **kwargs):
    for key, value in kwargs.iteritems():
        string = string.replace(key, value)
    return string


def replace_all(filename, **kwargs):
    dst = replace_in_string(filename, **kwargs)
    if os.path.isdir(filename):
        if filename != dst:
            shutil.move(filename, dst)
            filename = dst
        for f in os.listdir(filename):
            replace_all(os.path.join(filename, f), **kwargs)
    else:
        if filename == dst:
            tmp = '%s.tmp.%d' % (filename, time.time())
            shutil.move(filename, tmp)
            filename = tmp
        replace_in_file(filename, dst, **kwargs)
        os.remove(filename)


def main():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('--name', '-n',
        default='example', required=True,
        help='Name of the project to create')

    args = argparser.parse_args()

    parts = args.name.split(' ')
    camel_name = ''.join(p.capitalize() for p in parts)
    lower_name = ''.join(p.lower()      for p in parts)

    dstdir = os.path.basename(lower_name)
    dstdir = os.path.join(os.getcwd(), dstdir)
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
