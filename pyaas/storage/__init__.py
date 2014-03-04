
from .initialize import initialize
from .record     import *

import pyaas

pyaas.argparser.add_argument('--db',
    help='Select storage engine')

pyaas.argparser.add_argument('--initdb',
    action='store_true',
    help='Initialize the database')
