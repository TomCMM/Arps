
import sys

def clear(module):
    """
    reload a module and reimport all its class
    """
    modulename=module.__name__
    reload(sys.modules[modulename])
    print("module reload : ", module)
    for attr in dir(sys.modules[modulename]):
        if not attr.startswith('_'):
            globals()[attr] = getattr(sys.modules[modulename], attr)


