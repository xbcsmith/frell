
NAME="@MODULE@"
VERSION = (0, 0, 1)

def get_version():
    return '.'.join(str(v) for v in VERSION)

def get_name():
    return NAME
