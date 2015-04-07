import base64

import getpass
import socket
import string

import os
import subprocess

import time
import datetime

import inspect


def find_exe(name):
    """
    Find an executable with the given name.
    :param name:
    :return:
    """
    for path in os.getenv('PATH').split(os.pathsep):
        for ext in ('', '.exe', '.cmd', '.bat', '.sh'):
            full_path = os.path.join(path, name + ext)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path
    return None


def generate_version_file(infile='version.py.in', outfile='version.py', **kwargs):
    """
    Using input file, generate an output file with the version info for this package.
    This should generally be used in setup.py to generate build stamp info.
    :param infile:
    :param outfile:
    :param kwargs:
    :return:
    """

    if not os.path.exists(outfile) and os.path.exists(infile):
        now = datetime.datetime.now()
        repo_hash = ''
        git_path = find_exe('git')
        if git_path is not None:
            git_cmd = [find_exe('git'), 'log', '--format=%h', '-1']
            repo_hash = subprocess.Popen(git_cmd, stdout=subprocess.PIPE).communicate()[0].strip()
        if repo_hash.strip() == '':
            repo_hash = '{now.hour}.{now.minute}.{now.second}'.format(now=now)

        sub_dict = {
            'repo_hash': repo_hash,
            'build_date': '{now.year}.{now.month}.{now.day}'.format(now=now),
            'build_time': '{now.hour}.{now.minute}.{now.second}'.format(now=now),
            'build_host': socket.gethostname(),
            'build_user': getpass.getuser()
        }
        sub_dict.update(**kwargs)

        with open(infile) as version_in:
            version_data = version_in.read()
            version_final = string.Template(version_data).safe_substitute(sub_dict)

        with open(outfile, 'w') as version_out:
            version_out.write(version_final)

    return outfile if os.path.exists(outfile) else None


def generateCookieSecret(path):
    secret = base64.b64encode(os.urandom(32))
    with open(path, 'w') as fp:
        fp.write(secret)
    return secret


def getParent():
    # inspect who called this function
    frames = inspect.getouterframes(inspect.currentframe())
    # get the caller frame
    frame = frames[-1]
    # get the path of the caller
    script = os.path.abspath(frame[1])

    return script
