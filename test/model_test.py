#!/usr/bin/env python
import sys
import logging
import epdb
from crufter.error import debugExceptHook
from crufter.model import File
from crufter.model import Source
from crufter.model import Tag
from crufter.model import Action
from crufter.model import ActionValues
from crufter.model import Package

sys.excepthook = debugExceptHook

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

fn = {
        'name': 'test.so',
        'mode': '0644',
        'owner': 'sas',
        'group': 'sas',
        'type': 'file'
    }

files = [ File(**fn) ]


source = {  'archive': 'test-0.0.1-lax.zip',
            'destination': '/opt/Home',
            'files': files,
            'source': 'git://testing'
            }


sources = [ Source(**source) ]

tagtype = { 'tag' : 'symlink'}

tag = Tag(**tagtype)

symlink =  { "key" : "symlink", "value" : "path/to/symlink"} 
flhndle = { "key" : "file", "value" : "path/to/symlink2"}

actionvalues =  [   ActionValues(**symlink),
                    ActionValues(**flhndle)
                ]

actiontype = { "action" : "create", "tag" : tag, "values" : actionvalues }

postinstall = [ Action(**actiontype) ]


package = { 'name': 'test',
            'description': 'Testing Example',
            'lang': 'en',
            'platform': 'lax',
            'postinstall': postinstall,
            'release': '1.sp0.test',
            'requires': 'test-requires',
            'sources': sources,
            'version': '0.0.1',
        }


#epdb.st()
test = Package(**package)

print "Name", test.name
print "Version", test.version
print "PostInstallActions:", test.postinstall
print "Sources:", test.sources
print "Requires", test.requires
test.version = '0.0.2'
test.requires = 'test-requires-updated'
updatedsource = sources[0]
updatedsource.archive = 'test-0.0.2-lax.zip'
sources = [ updatedsource ]

print "Name", test.name
print "Version", test.version
print "PostInstallActions:", test.postinstall
print "Sources:", test.sources
print "Requires", test.requires

print test.asJSON()


badkey =  { "key" : "trex", "value" : "path/to/symlink"} 
badvalues = ActionValues(**badkey)
