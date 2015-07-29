#!/usr/bin/env python

import base_test
import logging
logger = logging.getLogger('debuger')

# TEST SPECIFIC IMPORTS

def runtest(test_dir):
    return 0

def main(testname, test_dir, args):
    logger.info('Calling %s with %s' % (testname, str(args)))
    runtest(test_dir)

if __name__ == "__main__":
    import sys
    testname = 'template'
    test_dir = base_test.project_dir(testname)
    main(testname, test_dir, sys.argv)
    #import epdb;epdb.st()

