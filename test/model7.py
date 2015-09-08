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

    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
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
    def set(self, key, value):
        self.__setitem__(key, value)

    def _expanded(self):
        pd = {}
        for x, y in self.__dict__.iteritems():
            if not x.startswith('_'):
                if isinstance(y, basestring):
                    pd[x] = y
                elif isinstance(y, dict):
                    pd[x] = dict((k, v._expanded()) if isinstance(v, Model)
                                        else (k,v) for k, v in y.iteritems())
                elif isinstance(y, (list, tuple)):
                    pd[x] = [ z._expanded() if isinstance(z, Model)
                                        else z for z in y ]
                elif isinstance(y, Model):
                    pd[x] = y._expanded()
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


class Package(Model):

    @property
    def nvr(self):
        return '%s-%s-%s' % (self.name, self.version, self.release)

    @classmethod
    def fromDict(cls, args):
        assert isinstance(args, dict), "Requires a dict"

        def _handle_objects(value):
            if isinstance(value, basestring):
                return value
            elif isinstance(value, (list, tuple)):
                return  [ _handle_objects(z) if not isinstance(z, Model)
                                            else z for z in value ]
            elif isinstance(value, dict):
                return dict((k, _handle_objects(v)) if not isinstance(v, Model)
                                            else (k,v) for k, v in value.iteritems())
            elif isinstance(value, Model) or value is None:
                return value
            else:
                return Model(value)

        def _handle_list(value):
            new = []
            for z in value:
                if isinstance(z, dict):
                   new.append(_handle_objects(z))
                if isinstance(z, (list, tuple)):
                    new.append(_handle_objects(z))
                else:
                    new.append(z)
            return new

        def _handle_dict(value):
            new = {}
            for k, v in value.iteritems():
                if isinstance(v, dict):
                    new[k] =  _handle_objects(v)
                if isinstance(v, (list, tuple)):
                    new[k] = _handle_objects(v)
                else:
                    new[k] = v
            return new

        new = {}
        for key, value in args.iteritems():
            if isinstance(value, dict):
                new[key] = _handle_dict(value)
            elif isinstance(value, (list, tuple)):
                new[key] = _handle_list(value)
            else:
                new[key] = value

        return cls(**new)
