
NAME="@NAME@"
MODULE="@MODULE@"
VERSION = (0, 0, 1)

def get_version():
    return '.'.join(str(v) for v in VERSION)

def get_name():
    return NAME

def get_module():
    return MODULE
