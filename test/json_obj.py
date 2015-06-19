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

class Location(StorageObject):
    city = Field('city', str)
    zip = Field('zip', str)

class User(StorageObject):
    username = Field('username', str)
    uid = Field('uid', int)
    location = Field('location', Location)

class JsonObject(StorageObject):
    tag = Field('tag', str)
    created_by = Field('created_by', User)
    modified_by = Field('modified_by', User)

j = JsonObject({'a' : 1, 'created_by' : {'username' : 'miiban', 'uid' : 500}})
print "Created by:", j.created_by
print "Modified by:", j.modified_by
print "Modified by username:", j.modified_by.username
j.modified_by.username = 'bcsmit'
j.modified_by.uid= 501
print "Modified by username:", j.modified_by.username
print "Modified by zip:", j.modified_by.location.zip
j.modified_by.location.zip = 27511
print "Modified by zip:", j.modified_by.location.zip
