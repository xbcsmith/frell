#!/usr/bin/env python
import sys
import logging
import epdb
import yaml
from yaml import CDumper as Dumper
from yaml import CLoader as Loader
from error import debugExceptHook
from model import File
from model import Source
from model import Tag
from model import Action
from model import ActionValues
from model import Package

sys.excepthook = debugExceptHook

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

filelist = [    '/lib/frell/model.py',
                '/lib/frell/converter.py',
                '/lib/model.py',
                '/share/frell/docs/README.md',
                '/frell.conf',
                '/bin/frell',
            ]

files = []

for fn in filelist:
    mode = '0644'
    if fn.startswith('/bin'):
        mode = '0755'
    fn = {
        'name': fn,
        'mode': mode,
        'owner': 'default',
        'group': 'default',
        'type': 'file'
        }

    files.append(File(**fn))


source = {  'archive': 'frell-0.0.1.zip',
            'destination': '/opt/frell',
            'files': files,
            'source': 'git://testing'
            }


sources = [ Source(**source) ]

tagtype = { 'tag' : 'symlink'}

tag = Tag(**tagtype)

symlink =  { "key" : "symlink", "value" : "/opt/bin/frell"} 
flhndle = { "key" : "file", "value" : "/opt/bin/frell.test"}

actionvalues =  [   ActionValues(**symlink),
                    ActionValues(**flhndle)
                ]

actiontype = { "action" : "create", "tag" : tag, "values" : actionvalues }

postinstall = [ Action(**actiontype) ]


package = { 'name': 'frell',
            'description': 'Frelling Test Example',
            'lang': 'en',
            'platform': 'linux',
            'postinstall': postinstall,
            'release': '1.EL.test',
            'requires': 'test-requires',
            'sources': sources,
            'version': '0.0.1',
        }


#epdb.st()
test = Package(**package)

blob = yaml.load(test.asJSON(), Loader=Loader)
print yaml.dump(blob, default_flow_style=False, Dumper=Dumper)
