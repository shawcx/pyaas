
from .application import Application

import pyaas

pyaas.argparser.add_argument('--name',
    help='Specify a name for the instance')

pyaas.argparser.add_argument('--address', '-a',
    help = 'Interface to bind to')

pyaas.argparser.add_argument('--port', '-p',
    type=int,
    help='Port to bind to')

pyaas.argparser.add_argument('--newcookie',
    action='store_true',
    help='Generate a new cookie')
