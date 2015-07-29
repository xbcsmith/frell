import logging
import logging.config
import os
import sys
import constants

logcfg =  'logger.ini'
logcfg_path = None

try:
    logcfg_path = os.path.join('/etc/' % constants.get_name(), logcfg)
    assert os.path.exists(logcfg_path)
except AssertionError:
    logcfg_path = None

if not logcfg_path:
    try:
        logcfg_path = os.path.realpath(os.path.dirname(__file__) + os.path.sep + logcfg)
        assert os.path.exists(logcfg_path)
    except AssertionError:
        logcfg_path = None

if logcfg_path is None:
    pythonpath = os.environ.get('PYTHONPATH')

    if pythonpath and os.path.exists(pythonpath):
        print "Walking the PYTHONPATH looking for %s" % logcfg
        for path, dirs, files in os.walk(pythonpath):
            for fn in files:
                if fn == logcfg:
                    logcfg_path = os.path.join(path, fn)
                    break


if not logcfg_path:
    print "Walking the sys.path looking for %s" % logcfg
    for pythonpath in sys.path:
        for path, dirs, files in os.walk(pythonpath):
            for fn in files:
                if fn == logcfg:
                    logcfg_path = os.path.join(path, fn)
                    break

if not logcfg_path:
    msg = "Error No clue where to find %s" % logcfg
    raise IOError, msg
    import epdb;epdb.st()

logging.config.fileConfig(logcfg_path)
logger = logging.getLogger(__name__)
