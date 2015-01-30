
import collections
import logging

import pyaas

moduleImports = dict(
    auth    = 'pyaas.web.auth',
    storage = 'pyaas.storage.engines',
    cache   = 'pyaas.storage.cache',
    )


def load():
    modules = dict(pyaas.config.items('modules'))
    for module in modules:
        try:
            modulePath = pyaas.module.moduleImports[module]
        except KeyError:
            logging.error('Unknown module: %s', module)
            continue

        # on import PyaasModules register themselves
        __import__(pyaas.module.moduleImports[module])

    for module, moduleClass in pyaas.module.PyaasModule.registry.items():
        moduleClass.load()

    return


class RegisterModuleMeta(type):
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            # this is the base class.  Create an empty registry
            cls.registry = {}
        else:
            # this is a derived class.  Add cls to the registry
            cls.registry[name] = cls

        super(RegisterModuleMeta, cls).__init__(name, bases, dct)


class PyaasModule(object):
    PKG_PATH = 'pyaas'
    CLASSES = collections.defaultdict(dict)

    __metaclass__ = RegisterModuleMeta

    @classmethod
    def load(cls):
        raise NotImplementedError

    @classmethod
    def loadModule(cls, moduleName):
        classes = cls.CLASSES[cls.__name__]

        try:
            return classes[moduleName]
        except KeyError:
            # try to load the module
            pass

        # then try loading a pyaas module first
        try:
            path = cls.PKG_PATH + '.' + moduleName
            module = __import__(path)
        except ImportError:
            # try loading a user-supplied module next
            try:
                path = moduleName
                module = __import__(path)
            except ImportError:
                raise pyaas.error('Unknown module: %s', moduleName)

        subPackageName = path
        for subPackageName in subPackageName.split('.')[1:]:
            module = getattr(module, subPackageName)

        classname = subPackageName.capitalize()

        moduleClass = getattr(module, classname, None)
        if moduleClass is None:
            try:
                moduleClass = getattr(module, 'Database')
            except AttributeError:
                raise pyaas.error('Bad module: %s', moduleName)

        classes[moduleName] = moduleClass

        return moduleClass
