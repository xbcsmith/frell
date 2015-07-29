
import traceback
import epdb


class @NAME@Error(Exception):
    "Base class"

class InvalidYamlFound(@NAME@Error):
    "Raised when YAML is invalid"

class RepositoryError(@NAME@Error):
    "Raised when a repository error is caught"

class TemplateNotFound(@NAME@Error):
    "Raise when a template is not found"

def debugExceptHook(type, value, tb):
    print "T-Rex Hates %s" % type.__name__
    print str(type)
    traceback.print_exception(type, value, tb)
    epdb.post_mortem(tb)
