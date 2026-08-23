import json

class JsonableMixin:
    def json_default(value):
        import datetime, uuid
        if isinstance(value, datetime.datetime):
            return dict(year=value.year, month=value.month, day=value.day, hour=value.hour, minute=value.minute)
        elif isinstance(value, datetime.date):
            return dict(year=value.year, month=value.month, day=value.day)
        elif isinstance(value, uuid.UUID):
            return dict(hex=value.hex)
        else:
            return value.__dict__

    def asJSON(self):
        j = json.dumps(self, default=self.json_default, sort_keys=True, indent=4)
        return j

