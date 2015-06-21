import logging

log = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

class StorageObject(object):
    def __init__(self, storage):
        self._dict = storage

    def get(self, fieldName):
        return self._dict.get(fieldName)

    def set(self, fieldName, value):
        return self._dict.__setitem__(fieldName, value)

class Field(object):
    def __init__(self, fieldName, fieldType):
        self.fieldName = fieldName
        self.fieldType = fieldType

    def __get__(self, instance, owner):
        log.debug("Calling __get__ for %s", self.fieldName)
        if isinstance(instance, (list, tuple)):
            return [ Field(x) for x in instance ]
        val = instance._dict.get(self.fieldName)
        if issubclass(self.fieldType, (int, str)):
            return val
        if val is None:
            val = instance._dict[self.fieldName] = {}
        return self.fieldType(val)

    def __set__(self, instance, value):
        log.debug("Calling __set__ for %s", self.fieldName)
        if isinstance(instance, StorageObject):
            return instance.set(self.fieldName, value)
        instance._dict[self.fieldName] = value

class Value(StorageObject):
    key = Field('key', str)
    value = Field('value', str)

class Tag(StorageObject):
    _items = [  'symlink',
                'registry_key',
                'user',
                'group',
                'directory',
                'file',
                'modify'
                ]
    tag = Field('tag', str)

class Action(StorageObject):
    _items = [ 'create', 'delete', 'modify' ]
    action = Field('action', str)
    tag = Field('tag', Tag)
    value = Field('value', [Value])



test = Action({ "action" : "create", 
                "tag" : "symlink",
                "value" : {"path/to/file" : "path/to/symlink"},
                })

print "Action type:", test.action
print "Tag type:", test.tag
print "Value", test.value
test.action = 'delete'
test.tag = Tag('file')
test.value = {"file" : "path/to/symlink"} 
print "Action type:", test.action
print "Tag type:", test.tag.tag
print "Values", test.values
