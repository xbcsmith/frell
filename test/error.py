
import traceback
import epdb

def debugExceptHook(type, value, tb):
    print "T-Rex Hates %s" % type.__name__
    print str(type)
    traceback.print_exception(type, value, tb)
    epdb.post_mortem(tb)
