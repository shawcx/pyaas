
import sys
import os

import __main__

# a generic error class for throwing exceptions
class error(Exception):
    def __init__(self, fmt, *args):
        self.str = fmt % args

    def __str__(self):
        return self.str

root = os.path.abspath(sys.prefix)

def setroot(newroot):
    global root
    root = newroot

    # the root of the package directory
    #root = os.path.dirname(__file__)
    #root = os.path.join(root, 'data')

from . import settings
from . import util
from . import server
