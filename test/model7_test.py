#!/usr/bin/env python

import os 
import tempfile
import sys
import yaml
import jsonschema


from error import debugExceptHook
sys.excepthook = debugExceptHook


from model6 import Package


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

import collections

class Model(collections.MutableMapping):

    _marker = object()

    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))

    def __setitem__(self, key, value):
        if isinstance(value, (list, tuple)):
            value = [ Model(**z) if isinstance(z, dict) 
                                                else z for z in value ]
        elif isinstance(value, dict) and not isinstance(value, Model):
            value = Model(**value)
        self.__dict__[key] =  value

    def __getitem__(self, key):
        result = self.get(key, self._marker)
        if result is self._marker:
            result = Model()
            super(Model, self).__setitem__(self, key, result)
        return result

    __setattr__ = __setitem__
    __getattr__ = __getitem__


    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return '{0}, Model({1})'.format(super(Model, self).__repr__(),
                                  self.__dict__)

    def serialize(self):
        pd = {}
        for x, y in self.__dict__.iteritems():
            if not x.startswith('_'):
                if isinstance(y, basestring):
                    pd[x] = y
                elif isinstance(y, dict):
                    pd[x] = dict((k, v.serialize()) if isinstance(v, Model)
                                        else (k,v) for k, v in y.iteritems())
                elif isinstance(y, (list, tuple)):
                    pd[x] = [ z.serialize() if isinstance(z, Model)
                                        else z for z in y ]
                elif isinstance(y, Model):
                    pd[x] = y.serialize()
                else:
                    pd[x] = y
        return pd

    def merge(self, other):
        assert isinstance(other, self.__class__)
        for key, value in other.iteritems():
            svalue = getattr(self, key)
            if isinstance(value, Model):
                if isinstance(svalue, Model):
                    svalue.merge(value)
                elif not svalue:
                    setattr(self, key, value)
            elif isinstance(value, (list, tuple)):
                if not svalue:
                    setattr(self, key, value)
                else:
                    for i, v in enumerate(value):
                        if i > len(svalue):
                            svalue.append(v)
                        elif isinstance(svalue[i], Model):
                            svalue[i].merge(v)
                        else:
                            svalue[i] = v
            else:
                if not svalue:
                    setattr(self, key, value)

       

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
