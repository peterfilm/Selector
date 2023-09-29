import os
from modules.api import conf

def raw_finder(value):
    name_path = os.path.join(conf['PATH'], value.split('.')[0].lower())
    if value.split('.')[-1].lower() in conf['JPEGS']:
        for i in conf['RAW_FORMATS']:
            name = os.path.normpath(name_path + '.' + i.lower())
            if os.path.exists(name):
                return True
    return False