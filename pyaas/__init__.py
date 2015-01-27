
from .version import VERSION

# a generic error class for throwing exceptions
class error(Exception):
    def __init__(self, fmt, *args):
        self.str = fmt % args

    def __str__(self):
        return self.str


from . import util
from . import settings
from . import module

from .settings import init

prefix      = None
namespace   = None
paths       = None
db          = None
cache       = None
