
VERSION = '0.4.4'

# a generic error class for throwing exceptions
class error(Exception):
    def __init__(self, fmt, *args):
        self.str = fmt % args

    def __str__(self):
        return self.str


from . import settings
from . import util
from . import server
from . import module
from .util import init

prefix      = None
namespace   = None
paths       = None
db          = None
cache       = None
