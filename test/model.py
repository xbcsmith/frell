class AbstractModel(object):
    _model = {}

    def __init__(self):
        self._update()

    @classmethod
    def _str(cls, obj):
        if isinstance(obj, unicode):
            return obj.encode('ascii')
        if isinstance(obj, list):
            return [ cls._str(x) for x in obj ]
        if isinstance(obj, dict):
            return dict((cls._str(x), cls._str(y))
                for (x, y) in obj.items())
        return obj

    def _update(self):
        self.__dict__.update(self._str(self._model))
        return self

    def update(self, **kwargs):
        self._update(kwargs)


class Test(AbstractModel):
    _model = { 'test' : [
                { 'action' : None, 
                  'tags'  : [],
                  'values' : [{'key' : None, 'value' : None}],
                },
                ],
            }

