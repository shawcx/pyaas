#!/usr/bin/env python

import sys
import os
import atexit
import signal
import time
import inspect
import logging

import pyaas


pyaas.argparser.add_argument('daemon',
    metavar='(start|stop|restart)',
    help='Control the state of the service')

pyaas.argparser.add_argument('--instance',
    help='Name an instance to allow multiple copies to run')


class Daemonize(object):
    STDIN  = os.path.devnull
    STDOUT = os.path.devnull
    STDERR = os.path.devnull

    def __init__(self, entry, *args, **kwds):
        self.entry = entry
        self.args  = args
        self.kwds  = kwds

        script = pyaas.util.getParent()
        # get the filename of the caller
        script = os.path.basename(script)

        instance = pyaas.args.instance or 'server'

        self.pidfile = '/tmp/pyaas-{}-{}-{}.pid'.format(script, entry.func_name, instance)

        if 'start' == pyaas.args.daemon:
            self.start()
        elif 'stop' == pyaas.args.daemon:
            self.stop()
        elif 'restart' == pyaas.args.daemon:
            self.restart()
        else:
            raise pyaas.error('Unknown daemon option')

    def daemonize(self):
        if pyaas.args.debug:
            logging.debug('Staying in the foreground')
            return

        try:
            pid = os.fork()
        except OSError as e:
            logging.critical('EXCEPTION: os.fork: %d (%s)', e.errno, e.strerror)
            sys.exit(-1)

        if pid > 0:
            sys.exit(0)

        # clear environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # fork again
        try:
            pid = os.fork()
        except OSError as e:
            logging.critical('EXCEPTION: os.fork: %d (%s)', e.errno, e.strerror)
            sys.exit(-1)

        if pid > 0:
            sys.exit(0)

        # redirect file handles
        sys.stdout.flush()
        sys.stderr.flush()

        stdin  = open(self.STDIN,  'r'    )
        stdout = open(self.STDOUT, 'a+'   )
        stderr = open(self.STDERR, 'a+', 0)

        os.dup2(stdin.fileno(),  sys.stdin.fileno() )
        os.dup2(stdout.fileno(), sys.stdout.fileno())
        os.dup2(stderr.fileno(), sys.stderr.fileno())

        # write pidfile
        #atexit.register(self.delpid)
        def atexit_callback():
            try:
                os.remove(self.pidfile)
            except Exception as e:
                logging.warn('Unable to remove PID file: %s', self.pidfile)

        def signal_callback(signum, frame):
            if signum == signal.SIGTERM:
                sys.exit(0)

        atexit.register(atexit_callback)

        signal.signal(signal.SIGTERM, signal_callback)

        with open(self.pidfile, 'w') as fp:
            fp.write('{}'.format(os.getpid()))

    def _getpid(self):
        pid = None

        if os.path.isfile(self.pidfile):
            try:
                pid = open(self.pidfile, 'r')
                pid = int(pid.read())
            except IOError:
                # TODO: complain not being able to read file
                pid = None
            except ValueError:
                # TODO: complain about invalid value
                pid = None

        return pid

    def start(self):
        pid = self._getpid()

        if pid:
            logging.error('Daemon appears to be running')
            sys.exit(-1)

        # Start the daemon
        self.daemonize()

        pyaas.module.load()

        self.entry(*self.args, **self.kwds)

    def stop(self):
        pid = self._getpid()

        if not pid:
            logging.info('Daemon appears to not be running')
            return

        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno != 3:
                logging.warn('Error stopping process: %s', e)
                return

        count = 0
        while count < 100:
            try:
                os.kill(pid, 0)
                time.sleep(0.1)
                count += 1
            except OSError as e:
                if e.errno != 3:
                    logging.warn('Error stopping process: %s', e)
                    return
                else:
                    break

        if count == 100:
            logging.warn('Timeout stopping process')
            return

        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def restart(self):
        self.stop()
        self.start()
