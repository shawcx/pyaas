
import os

from .version import VERSION

from . import io
from . import util
from . import module
from . import settings
from . import module

# a generic error class for throwing exceptions
class error(Exception):
    def __init__(self, fmt, *args):
        self.str = fmt % args

    def __str__(self):
        return self.str


class Paths(object):
    def __getattr__(self, attribute):
        try:
            return object.__getattribute__(self, attribute)
        except AttributeError:
            return os.path.join(prefix, attribute, namespace)

    def __call__(self, toplevel, *args):
        return os.path.join(prefix, toplevel, namespace, *args)


paths       = Paths()
prefix      = ''
namespace   = ''
cache       = None