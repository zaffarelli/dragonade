def chiaroscuro_default(value):
    import datetime, uuid
    if isinstance(value, datetime.datetime):
        return dict(year=value.year, month=value.month, day=value.day, hour=value.hour, minute=value.minute)
    elif isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    elif isinstance(value, uuid.UUID):
        return dict(hex=value.hex)
    else:
        return value.__dict__

class ChiaroscuroMixin:
    """
    Mixin for Chiaroscuro support in data exchange between front and back
    """
    _data = {}
    _co_str = ""

    def chiaroscuro(self):
        # print(f"{self.__class__.__name__} è chiaroscuro")
        pass

    def model_to_data(self):
        import json
        self._co_str = json.dumps(self, default=chiaroscuro_default, sort_keys=True, indent=4)
        self._data = json.loads(self._co_str)
        self.co_push()
        self.co_update()
        # print(self._data)
        return self._co_str

    # def co_push(self):
    #     print("Chiaroscuro push")

    def co_update(self):
        import json
        self._co_str = json.dumps(self._data, default=chiaroscuro_default, sort_keys=True, indent=4)