
global GLOBALS_DICT
GLOBALS_DICT = {}

def _init():
    """init"""
    # global GLOBALS_DICT
    GLOBALS_DICT = {}
 
 
def set(name, value):
    """set"""
    try:
        GLOBALS_DICT[name] = value
        return True
    except KeyError:
        return False
 
 
def get(name):
    """get"""
    try:
        return GLOBALS_DICT[name]
    except KeyError:
        return "Not Found"