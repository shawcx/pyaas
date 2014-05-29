
import sys
import os

VERSION = '0.3.5'

# a generic error class for throwing exceptions
class error(Exception):
    def __init__(self, fmt, *args):
        self.str = fmt % args

    def __str__(self):
        return self.str


from . import settings
from . import util
from . import server

util.setPrefix()
util.setNameSpace('')
