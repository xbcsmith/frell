#!/usr/bin/env python

import os 
import tempfile
import sys
import yaml
import jsonschema


from error import debugExceptHook
sys.excepthook = debugExceptHook


from model7 import Model


PACKAGE = {'buildrequires': [],
 'changelog': {'date': 'Sun Jun 28 2015',
               'entry': 0,
               'msg': 'Test Message',
               'user': 'Test test@foo.com'},
 'description': 'Testing Example',
 'lang': 'en',
 'name': 'test',
 'package': 'rpm',
 'platform': 'lax',
 'platform_id': None,
 'postinstall': [{'action': 'create',
                  'tag': {'tag': 'symlink'},
                  'values': [{'key': 'symlink',
                              'value': 'path/to/symlink'},
                             {'key': 'file',
                              'value': 'path/to/symlink2'}]}
                ],
 'preinstall': None,
 'provides': [],
 'release': '1.sp0.test',
 'requires': [ 'test-requires' ],
 'sources': [{'archive': 'test-0.0.2-lax.zip',
              'destination': '/opt/Home',
              'files': [{'group': 'sas',
                         'mode': '0644',
                         'name': 'test.so',
                         'owner': 'sas',
                         'sha1': None,
                         'type': 'file'}],
              'source': 'git://testing'}],
 'version': '0.0.2'}


def readSchema(filename):
    blob = ''
    with open(filename, 'r') as fh:
        blob = fh.read()
    return yaml.safe_load(blob)
       

def main(args):
    '''
    Load schema.schema
    Create Package
    Debug
    '''
    schema = readSchema('schema.schema')
    resolver = jsonschema.RefResolver.from_schema(schema)

    pkg = Model(PACKAGE)

    import epdb;epdb.st()

if __name__ == "__main__":
    main(sys.argv)
