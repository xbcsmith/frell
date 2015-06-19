class AbstractModel(object):
    _model = { 'abstract' : { 'method' : None } }

    def __init__(self):
        self._update()

    def _update(self):
        for key, value in self._model.iteritems():
            self._name = key.capitalize()
            if isinstance(value, dict):
                for k, v in value.iteritems():
                    if isinstance(v, (list, tuple)):
                        setattr(self, k, [AbstractModel(x) if isinstance(x, dict)
                                    else x for x in v]) 
                    else:
                        setattr(self, k, AbstractModel(v) if isinstance(v, dict) else v)

        #self.__dict__.update(self._str(self._model))

    def _update_model(self, data):
        for k, v in data.iteritems():
            self._model.update(dict(k,v) if isinstance(v, dict) else v)

    def update(self, data):
        self._update()

    def __repr__(self):
        return '%s' % self._name


class Test(AbstractModel):
    _model = { 'test' : {   'action' : None, 
                            'tags'  : [],
                            'values' : [],
                    }
                }

class Action(AbstractModel):
    _model = { 'action' : { 'action': None,
               'tags': [],
               'values': [ {'key': None, 
                            'value': None},
                        ]
                }
            }




class File(AbstractModel):
    _model = { 'file' : {
                'group': 'default',
                'md5': None,
                'mode': '0755',
                'name': None,
                'owner': 'default',
                'type': None }
            }

class Source(AbstractModel):
    _model = { 'source' : { 'archive': None,
                            'destination': None,
                            'files': [],
                            'source': None
                    }
            }
                        
class Changelog(AbstractModel):
    _model = { 'changelog': [{  'date': None, 
                                'entry': None, 
                                'msg': None, 
                                'user': None}
                            ],
                }

class Package(AbstractModel):
    _model = { 'package' : {
                 'buildrequires': [],
                 'changelog': [{'date': None, 'entry': None, 'msg': None, 'user': None}],
                 'description': '',
                 'lang': None, # en
                 'name': None, 
                 'platform': None,
                 'platform_id': None,
                 'postinstall': [],
                 'preinstall': [],
                 'provides': [],
                 'release': None,
                 'requires': [],
                 'sources': [],
                 'version': None
                }
        }

class Actions(AbstractModel):
    _model = { 'actions': [
                 {'action': 'create',
                  'tags': ['symlink', 
                           'registry_key',
                           'user',
                           'group',
                           'directory',
                           'file'],
                  'values': [{'key': 'file', 'value': 'path/to/symlink'},
                             {'key': 'regkey','value': 'HKEY/LOCATION)'},
                             {'key': 'name', 'value': 'uid'},
                             {'key': 'name', 'value': 'gid'},
                             {'key': 'mode', 'value': 'path/to/directory'},
                             {'key': 'mode', 'value': 'path/to/file'}]},
                 {'action': 'delete',
                  'tags': ['symlink',
                           'registry_key',
                           'user',
                           'group',
                           'directory',
                           'file'],
                  'values': [{'key': None, 'value': 'path/to/symlink'},
                             {'key': 'regkey','value': '/HKEY/LOCATION)'},
                             {'key': 'name', 'value': 'uid'},
                             {'key': 'name', 'value': 'gid'},
                             {'key': None, 'value': 'path/to/directory'},
                             {'key': None, 'value': 'path/to/file'}]},
                 {'action': 'modify',
                  'tags': ['permissions'],
                  'values': [{'key': 'mode', 'value': 'path/to/directory'},
                             {'key': 'mode', 'value': 'path/to/file'}]}],
    }
