import logging

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

import collections

class Model(collections.MutableMapping):

    model = {}
    validate = {}

    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs)) 
        self.__dict__.update(self.model)

    def __getitem__(self, key):
        log.debug("Calling __getitem__ for %s", key)
        return self.__dict__[key]

    def __setitem__(self, key, value):
        log.debug("Calling __setitem__ for %s", value)
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
        return '{}, Model({})'.format(super(Model, self).__repr__(),
                                  self.__dict__)

    def items(self):
        return self.model.keys()

    def __validate__(self, key, value):
        valid = self.validate.get(key) or []
        if valid:
            try:
                if value in valid:
                    return value
            except Exception:
                raise 
        else:
            return value

class Value(Model):
    model = { 'key' : '' , 'value' : '' }

class Tag(Model):
    validate = { 'tag' : [ 'symlink',
                'registry_key',
                'user',
                'group',
                'directory',
                'file',
                'modify'
                ]}
    model = { 'tag': '' }

class Action(Model):
    validate = { 'action' : [ 'create', 'delete', 'modify' ] }
    model = { 'action' : '' , 'tag' : '' , 'values' : [] }

class Plan(Model):
    pass


