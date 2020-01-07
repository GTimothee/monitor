import inspect
import monitor
import traceback
import sys
from os.path import dirname
from time import gmtime, strftime


def get_module_dir():
    """ Locate current module directory.
    """
    exc_info = _dir = None 
    
    try:
        module_path = inspect.getfile(monitor)
        _dir = dirname(module_path)
        print(f'Using default log directory: {_dir}')
    except Exception as e:
        exc_info = sys.exc_info()
        print(f'Unable to retrieve module location.')
    finally:
        if exc_info:
            traceback.print_exception(*exc_info)
            del exc_info
    return _dir


def get_today_date():
    """ Format for dates compatible with that specified in the RFC 2822 Internet email standard
    """
    return strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())