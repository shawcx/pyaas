
import sys
import os

import __main__

# a generic error class for throwing exceptions
class error(Exception):
    def __init__(self, fmt, *args):
        self.str = fmt % args

    def __str__(self):
        return self.str

root = sys.prefix

def setroot(newroot):
    global root
    root = os.path.abspath(newroot)

from . import settings
from . import util
from . import server
