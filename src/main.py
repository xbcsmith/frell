
import os
from . import constants
from optparse import OptionParser

import logging
logger = logging.getLogger(__name__)

def main(args=None):

    _prog = constants.get_name()

    _usage = ('Usage: %prog <yaml file paths> -o <output_dir>')

    # Populate our options
    parser = OptionParser(version="%prog 0.0.1", usage=_usage)

    parser.add_option(  "-l", "--logfile", 
                        dest="logfile", 
                        default='%s.log' % _prog,
                        help="write log to FILE", 
                        metavar="FILE"
                    )

    parser.add_option(  '-v', '--verbose', 
                        dest='verbose', 
                        action='count', 
                        default=0,
                        help="Increase verbosity (specify multiple times for more)"
                    )

    parser.add_option(  '-d', '--dir', 
                        dest='_dir', 
                        action='store', 
                        default=None,
                        help="Specify directory to store outputs in"
                    )

    parser.add_option(  '--debug', 
                        dest='debug', 
                        action='store_true', 
                        default=False,
                        help="Increased Logging for troubleshooting"
                    )
    # Parse the arguments (defaults to parsing sys.argv).
    opts, args = parser.parse_args()

    if not args:
        import sys
        print >> sys.stderr, _usage.replace('%prog', _prog)
        sys.exit(1)

    verbose = opts.verbose
    logfile = opts.logfile
    default_template = opts.default_template

    if opts.debug:
        verbose = 3
    
    _dir = opts._dir

    if _dir:
        if not os.path.exists(_dir):
            os.makedirs(_dir)
    else:
        _dir = os.getcwd()


    results = []

    return results


if __name__ == '__main__':
    main()
