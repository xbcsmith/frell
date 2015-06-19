import json

class Model(object):
    _model = { 'model' : None }
    _json_data = None

    def __init__(self, json_data=None):
        if json_data and isinstance(self.json_data, basestring):
            json_data = json.loads(self.json_data)
        else:
            json_data = json.loads(str(self._model))   
        self._json_data = json_data
 
    def __getattr__(self, key):
        if key in self._json_data:
            if isinstance(self._json_data[key], (list, dict)):
                return Model(self._json_data[key])
            else:
                return self._json_data[key]
        else:
            raise Exception('There is no _json_data[\'{key}\'].'.format(key=key))
 
    def __repr__(self):
        out = self.__dict__
        return '%r' % (out['_json_data'])

    def update(self, json_data):
        if isinstance(json_data, basestring):
            json_data = json.loads(json_data)
        self._json_data = json_data

class AbstractModel(object):

    _json = None

    def __init__(self):
        if self._json:
            self.load()

    def _update(self, data):
        for k, v in data.iteritems():
            if isinstance(v, (list, tuple)):
                    setattr(self, k, [AbstractModel(x) if isinstance(x, dict) 
                                else x for x in v])
            else:
                setattr(self, k, AbstractModel(v) if isinstance(v, dict) else v)

    def __getitem__(self, val): 
        return self.__dict__[val]

    def load(self):
        with open(self._json, 'r') as stream:
            data = json.load(stream)
        self._update(data)       

    def update(self, data):
        self._update(data)

class Test(AbstractModel):

    _json = 'test.json'

class TestModel(Model):

    _model =  {
                "Test": [
                    {
                        "action": "create",
                        "tags": [
                            None
                        ],
                        "values": [
                            {
                                "key": None,
                                "value": None
                            }
                        ]
                    }
                ]
            }

