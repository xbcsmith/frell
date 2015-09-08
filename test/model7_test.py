#!/usr/bin/env python

import os 
import time
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
       

def test_construction():

    fn = {'name': 'test.so',
          'mode': '0644',
          'owner': 'foo',
          'group': 'foo',
          'type': 'file'
          }

    files = [ fn ]

    source = {'archive': 'test-0.0.1-linux.zip',
              'destination': '/opt/Home',
              'files': files,
              'source': 'git://testing'
              }

    sources = [ Model(**source) ]

    tag = {'tag': 'symlink'}

    symlink = {"key": "symlink", "value": "path/to/symlink"}
    flhndle = {"key": "file", "value": "path/to/symlink2"}

    actionvalues = [ symlink,
                     flhndle
                    ]

    actiontype = {"action": "create", "tag": tag, "values": actionvalues }

    postinstall = [ actiontype ]

    changelog = {'user': 'Joe Strummer <jstrummer@london.com>',
            'date': time.strftime('%a %b %d %Y'),
            'msg': 'Magnificent Seven Build System',
            'entry': 0,
            }


    package = {'name': 'test',
               'description': 'Testing Example',
               'lang': 'en',
               'platform': 'linux',
               'postinstall': postinstall,
               'release': '1.sp0.test',
               'requires': ['test-requires'],
               'sources': sources,
               'version': '0.0.1',
               'changelog': changelog,
               }

    pkg = Model(**package)

    return pkg


def test_update(pkg):

    sources = pkg.sources

    source = {'archive': 'test-0.0.2-linux.zip',
              'destination': '/opt/Home',
              'source': 'git://testing'
              }

    sources.append(Model(**source))

    pkg.version = '0.0.2'

    pkg.sources = sources

    pkg.changelog = {'user': 'Mick Jones <mickjones@calling.com>',
            'date': time.strftime('%a %b %d %Y'),
            'msg': 'Magnificent Seven Build System',
            'entry': 1,
            }

    return pkg

def main(args):
    '''
    Load schema.schema
    Create Package
    Debug
    '''
    schema = readSchema('schema.schema')
    resolver = jsonschema.RefResolver.from_schema(schema)

    pkg = Model(PACKAGE)

    pkg_test = test_construction()

    pkg_update = test_update(pkg_test)

    import epdb;epdb.st()

if __name__ == "__main__":
    main(sys.argv)
