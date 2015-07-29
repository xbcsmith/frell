import collections
import json

class Model(collections.MutableMapping):

    model = {}
    validate = {}

    def __init__(self, *args, **kwargs):
        self.__dict__.update(self.model)
        self.update(dict(*args, **kwargs)) 

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        if key in self.model:
            self.__dict__[key] = self.__validate__(key, value)
        else:
            self.__dict__[key] = value

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

    def items(self):
        return self.model.keys()

    def __validate__(self, key, value):
        valid = self.validate.get(key) or []
        if len(valid):
            try:
                assert value in valid
                return value
            except Exception, e:
                raise KeyError, e
        else:
            return value

    def _expanded(self):
        pd = {}
        for x, y in self.__dict__.iteritems():
            if not x.startswith('_'):
                if isinstance(y, basestring):
                    pd[x] = y
                elif isinstance(y, (list, tuple)):
                    pd[x] = [ z._expanded() if isinstance(z, collections.MutableMapping) else z for z in y]
                elif isinstance(y, collections.MutableMapping):
                    pd[x] = y._expanded()
                else:
                    pd[x] = y
        return pd

    def asJSON(self):
        return json.dumps(self._expanded())


class Value(Model):
    model = { 'key' : '' , 'value' : '' }

class Tag(Model):
    validate = { 'tag' : [ 'symlink',
                'registry_key',
                'user',
                'group',
                'directory',
                'file',
                'permissions'
                ]}
    model = { 'tag': '' }

class Action(Model):
    validate = { 'action' : [ 'create', 'delete', 'modify' ] }
    model = { 'action' : '' , 'tag' : '' , 'values' : [] }

class ActionValues(Value):
    validate = { 'key' : [ 'file', 'regkey', 'user', 'group', 'mode', 'symlink' ] }


class File(Model):
    model = {
                'group': 'default',
                'md5': None,
                'mode': '0755',
                'name': None,
                'owner': 'default',
                'type': None
            }

class Source(Model):
    model = {   'archive': None,
                'destination': None,
                'files': [],
                'source': None
            }


class Changelog(Model):
    model = {   'date': None,
                'entry': None,
                'msg': None,
                'user': None
            }

class Package(Model):
    validate = { 'platform' : [ 'linux', 'wx64', 'unk' ] }
    model = {
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

    @property
    def nvr(self):
        return '%s-%s-%s' % (self.name, self.version, self.release)


