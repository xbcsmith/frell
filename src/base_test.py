#!/usr/bin/env python

import os
import tempfile
import sys
sys.path.append('../')

import logger
logger = logger.getDebugLogger()

from errors import debugExceptHook
sys.excepthook = debugExceptHook

def project_dir(testname):
    proj_dir = '_'.join(['_test', testname])
    if proj_dir and not os.path.exists(proj_dir):
        os.makedirs(proj_dir)
    return tempfile.mkdtemp(dir=proj_dir)

def runtest(test_dir):
    logger.info('Base Test')
    logger.info('Test Dir : %s' % test_dir)
    return test_dir

def main(testname, test_dir, args):
    logger.info('Calling %s with %s' % (testname, str(args)))
    runtest(test_dir)

if __name__ == "__main__":
    testname = 'base'
    test_dir = project_dir(testname)
    main(testname, test_dir, sys.argv)

