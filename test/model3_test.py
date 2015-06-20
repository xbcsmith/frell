#!/usr/local/bin/python
from model3 import Test

data = { 'action' : 'create',
        'tags'  : 'foo',
        'values' : [ {'key' : 'fuz', 'value' : 'buz'},
                    {'key' : 'faz', 'value' : 'baz'},],
        }
    


test = Test()


import epdb;epdb.st()

