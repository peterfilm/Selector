import os
from modules.api import conf

def jpeg_finder(value):
    name_path = os.path.join(conf['PATH'], value.split('.')[0].lower())
    if value.split('.')[-1].lower() in conf['RAW_FORMATS']:
        for i in conf['JPEGS']:
            name = os.path.normpath(name_path + '.' + i.lower())
            if os.path.exists(name):
                return value + f' + {i.upper()}'
    return value


def jpeg_finder2(value):
    name_path = os.path.join(conf['PATH'], value.split('.')[0].lower())
    if value.split('.')[-1].lower() in conf['RAW_FORMATS']:
        for i in conf['JPEGS']:
            name = os.path.normpath(name_path + '.' + i.lower())
            if os.path.exists(name):
                return name
    return False