
import pyaas
import logging


def _loadModuleImpl(moduleName, defaultPath):
    """
    Based on a module impl name, attempt to load the python module
    If the module name is fully qualified, use that string only.  Otherwise,
    Prepend the defaultPath
    :param moduleName: module impl name (google or pgsql or my.module.module)
    :param defaultPath: default path to find built in module impls
    :return: The loaded python module
    """

    if '.' in moduleName:
        moduleName = moduleName
    else:
        # all auth mechanisms need to be in this path
        moduleName = defaultPath + '.' + moduleName

    try:
        module = __import__(moduleName)
    except ImportError:
        raise pyaas.error('Unknown module: "%s"', moduleName)

    for sub in moduleName.split('.')[1:]:
        module = getattr(module, sub)

    return module

def _loadModuleClass(clsname, moduleName, defaultPath):
    """
    Load the class within the module
    :param clsname: The name of the class within the package (Login, Cache, or Database)
    :param moduleName: module impl name (google or pgsql or my.module.module)
    :param defaultPath: default path to find built in module impls
    :return: The class
    """
    module = _loadModuleImpl(moduleName, defaultPath)
    try:
        cls = getattr(module, clsname)
    except AttributeError:
        raise pyaas.error('Failed to load class %s from %s', clsname, moduleName)
    return cls


def _initializeObject(obj, **options):
    """
    Attampts to invoke an initialize function/method on the given object
    :param obj:
    :param options:
    :return:
    """
    func = None
    if hasattr(obj, 'initialize'):
        f = getattr(obj, 'initialize')
        if callable(f):
            func = f
    if func is None and hasattr(obj, 'Initialize'):
        f = getattr(obj, 'Initialize')
        if callable(f):
            func = f

    if func is not None and func.__self__ is obj:
        func(**options)


class PyaasModule(object):
    """
    Defines a pyaas module.  Pyaas modules are parts of the system that may be configured
    and/or extended.  These are things like database engines, authentication systems or
    cache backends.
    Available modules are: storage, cache, and auth
    """
    def __init__(self, name=None, defaultPackage=None, className=None):
        self._name = name
        self._defaultPackage = defaultPackage
        self._className = className
        self._cls = None
        self._obj = None
        self._implName = None
        self._options = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def defaultPackage(self):
        return self._defaultPackage

    @defaultPackage.setter
    def defaultPackage(self, value):
        self._defaultPackage = value

    @property
    def className(self):
        return self._className

    @className.setter
    def className(self, value):
        self._className = value

    @property
    def implName(self):
        if self._implName is None:
            name = self.name
            if name in pyaas.args.__dict__:
                self._implName = pyaas.args.__dict__[name]
            elif pyaas.config.has_option('modules', name):
                self._implName = pyaas.config.get('modules', name)
        return self._implName

    @property
    def options(self):
        if self._options is None:
            impl = self.implName
            self._options = {}
            if pyaas.config.has_section(impl):
                self._options = dict(pyaas.config.items(impl))
                logging.debug('%s options: %s', self.name, self._options)
        return self._options

    def getInstance(self):
        if self._obj is None:
            cls = self.getClass()
            impl = self.implName

            if cls is None or impl is None:
                return None

            options = self.options
            self._obj = cls(**options)
            _initializeObject(self._obj)
        return self._obj

    def getClass(self):
        if self._cls is None:
            impl = self.implName
            if impl is None:
                return None

            self._cls = _loadModuleClass(self.className, impl, self.defaultPackage)
            if self._cls is None:
                return None

            _initializeObject(self._cls, **self.options)
        return self._cls

    def load(self, application=None):
        raise Exception("load not implemented!")




class Auth(PyaasModule):
    """
    Pyaas auth module
    """
    def __init__(self):
        super(Auth, self).__init__('auth', 'pyaas.handlers.auth', 'Login')

    def load(self, application=None):
        login = self.getClass()
        if login:
            # extend the patterns and settings accordingly
            application.patterns.extend([
                ( r'/login',  login                      ),
                ( r'/logout', pyaas.handlers.auth.Logout ),
                ])

            application.settings['login_url'] = '/login'

            logging.debug('Enabled authentication: %s', self.implName)


class Storage(PyaasModule):
    """
    Pyaas database module
    """
    def __init__(self):
        super(Storage, self).__init__('storage', 'pyaas.storage.engines', 'Database')

    def load(self, application=None):
        pyaas.db = self.getInstance()
        if pyaas.db:
            logging.debug('Enabled storage: %s', self.implName)


class Cache(PyaasModule):
    """
    Pyaas cache module
    """
    def __init__(self):
        super(Cache, self).__init__('cache', 'pyaas.storage.cache', 'Cache')

    def load(self, application=None):
        pyaas.cache = self.getInstance()
        if pyaas.cache:
            logging.debug('Enabled cache: %s', self.implName)


