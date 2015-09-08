#
# Copyright (c) SAS Institute Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import collections


class Model(collections.MutableMapping):

    _marker = object()

    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))

    def __setitem__(self, key, value):
        if isinstance(value, (list, tuple)):
            value = [ Model(**z) if isinstance(z, dict)
                                                else z for z in value ]
        elif isinstance(value, dict) and not isinstance(value, Model):
            value = Model(**value)
        self.__dict__[key] =  value

    def __getitem__(self, key):
        result = self.get(key, self._marker)
        if result is self._marker:
            result = Model()
            super(Model, self).__setitem__(self, key, result)
        return result

    __setattr__ = __setitem__
    __getattr__ = __getitem__

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

    def serialize(self):
        pd = {}
        for x, y in self.__dict__.iteritems():
            if not x.startswith('_'):
                if isinstance(y, basestring):
                    pd[x] = y
                elif isinstance(y, dict):
                    pd[x] = dict((k, v.serialize()) if isinstance(v, Model)
                                        else (k,v) for k, v in y.iteritems())
                elif isinstance(y, (list, tuple)):
                    pd[x] = [ z.serialize() if isinstance(z, Model)
                                        else z for z in y ]
                elif isinstance(y, Model):
                    pd[x] = y.serialize()
                else:
                    pd[x] = y
        return pd

    def merge(self, other):
        assert isinstance(other, self.__class__)
        for key, value in other.iteritems():
            svalue = getattr(self, key)
            if isinstance(value, Model):
                if isinstance(svalue, Model):
                    svalue.merge(value)
                elif not svalue:
                    setattr(self, key, value)
            elif isinstance(value, (list, tuple)):
                if not svalue:
                    setattr(self, key, value)
                else:
                    for i, v in enumerate(value):
                        if i > len(svalue):
                            svalue.append(v)
                        elif isinstance(svalue[i], Model):
                            svalue[i].merge(v)
                        else:
                            svalue[i] = v
            else:
                if not svalue:
                    setattr(self, key, value)

