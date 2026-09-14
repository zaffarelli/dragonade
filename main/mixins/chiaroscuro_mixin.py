

class ChiaroscuroMixin:
    """
    Mixin for Chiaroscuro support in data exchange between front and back
    """
    _data = {}
    _co_str = ""

    @property
    def type(self):
        return self.__class__.__name__



    def chiaroscuro(self):
        pass

    def chiaroscuro_default(self,value):
        import datetime, uuid
        if isinstance(value, datetime.datetime):
            return dict(year=value.year, month=value.month, day=value.day, hour=value.hour, minute=value.minute)
        elif isinstance(value, datetime.date):
            return dict(year=value.year, month=value.month, day=value.day)
        elif isinstance(value, uuid.UUID):
            return dict(hex=value.hex)
        else:
            return value.__dict__

    def model_to_data(self):
        import json
        self._co_str = json.dumps(self, default=self.chiaroscuro_default, sort_keys=True, indent=4)
        self._data = json.loads(self._co_str)
        self._data["type"] = self.type.lower()
        self.co_push()
        self.co_update()
        # print(self._data)
        return self._co_str

    def co_update(self):
        import json
        self._co_str = json.dumps(self._data, default=self.chiaroscuro_default, sort_keys=True, indent=4)