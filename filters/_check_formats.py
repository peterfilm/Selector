from modules.api import conf

def check_formats(value):
    a = conf['SIMPLE_FORMATS'].copy()
    a.extend(conf['RAW_FORMATS'])
    if value.lower() in a:
        return True
    return False