
from .initialize import initialize
from .records    import *

import pyaas

pyaas.argparser.add_argument('--db',
    help='Select storage engine')

pyaas.argparser.add_argument('--initdb',
    action='store_true',
    help='Initialize the database')
