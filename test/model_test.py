from model import Test


data = { 'test' : [
                { 'action' : 'create',
                  'tags'  : [ 'foo', 'bar' ],
                  'values' : [ {'key' : 'fuz', 'value' : 'buz'},
                               {'key' : 'faz', 'value' : 'baz'},],
                },
                ],
            }

test = Test()

import epdb;epdb.st()

test.update(**data)
