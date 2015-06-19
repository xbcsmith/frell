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

modeltest = TestModel()

import epdb;epdb.st()

