class AbstractModel(object):
    __slots__ = ( 'abstract', 'method' )

    def __init__(self, **kwargs):
        for s in self.__slots__:
            setattr(self, s, self._handle(s, kwargs.pop(s, None)))

    @classmethod
    def update(cls, **data):
        for s in cls.__slots__:
            setattr(cls, s, cls._handle(s, data.pop(s, None)))

    def get(self, flag):
        return getattr(self, flag)

    @classmethod
    def _handle(cls, s, v):
        if v is not None:
            if s in cls._model:
                spec = cls._model[s]
                if issubclass(spec, str):
                    if isinstance(v, str):
                        return v
                if issubclass(spec, AbstractModel):
                    return spec.update(v)
                if isinstance(spec, (list,tuple)):
                    for value in v:
                        klass = cls._model[s][0]
                        assert isinstance(v, klass)
                        return [ klass.update(x) for x in v ] 
        return v  

    def __iter__(self):
        return self.__slots__

    @property
    def items(self):
        '''return a list of all slots'''
        return self.__slots__

    def asJSON(self):
        json_data = {}
        for s in self.__slots__: 
            if isinstance(s, AbstractModel):
                json_data[s] = '%s' % getattr(self, s).asJSON()
            else:
                json_data[s] = getattr(self, s, None)
        return json_data



class Value(AbstractModel):        
    __slots__ = ( 'name', 'key', 'value' )    
    _model = {
                'key' : str,
                'value' : str,
            }

    def __repr__(self):
        return '(%s,%s)' % (self.key, self.value)

class Tag(AbstractModel):
    __slots__ = ( 'name', 'items', 'tag' )
    _items = [  'symlink', 
                'registry_key', 
                'user', 
                'group', 
                'directory', 
                'file', 
                'modify' 
                ]
    _model = {  'tag' : str }


class Action(AbstractModel):
    __slots__ = ( 'name', 'action', 'tag', 'values' )
    _items = [ 'create', 'delete', 'modify' ]
    _model = {
                'action': str,
                'tag': Tag,
                'values' : [ Value ]
            }


class Test(AbstractModel):
    __slots__ = ( 'name', 'action', 'tag', 'values' )

    _model = {
                 'action' : str, 
                 'tag'  : Tag,
                 'values' : [ Value ],
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
                 'changelog': [],
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
                             {'key': 'user', 'value': 'uid'},
                             {'key': 'group', 'value': 'gid'},
                             {'key': 'mode', 'value': 'path/to/file_or_directory'}]
                 },
                 {'action': 'delete',
                  'tags': ['symlink',
                           'registry_key',
                           'user',
                           'group',
                           'directory',
                           'file'],
                  'values': [{'key': 'regkey','value': '/HKEY/LOCATION)'},
                             {'key': 'user', 'value': 'uid'},
                             {'key': 'group', 'value': 'gid'},
                             {'key': 'file' , 'value': 'path/to/file_or_directory_or_symlink'},
                             ]},
                 {'action': 'modify',
                  'tags': ['permissions'],
                  'values': [{'key': 'mode', 'value': 'path/to/file_or_directory'}]
                            }
                            ],
    }
