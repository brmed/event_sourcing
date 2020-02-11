import datetime
import decimal
import json as _json


"""
This module consists of utilities to encode generics objects to json.

It extends the basic functionality of JSONEncoder by adding extra options to
Decimals, datetime and dates.

    +-------------------+---------------+
    | Python            | JSON          |
    +===================+===============+
    | dict              | object        |
    +-------------------+---------------+
    | list, tuple       | array         |
    +-------------------+---------------+
    | str               | string        |
    +-------------------+---------------+
    | int, float        | number        |
    +-------------------+---------------+
    | True              | true          |
    +-------------------+---------------+
    | False             | false         |
    +-------------------+---------------+
    | date, datetime    | string        |
    +-------------------+---------------+
    | decimal           | string        |
    +-------------------+---------------+
    | None              | null          |
    +-------------------+---------------+

SerializableDict also allows the serialization of sub-objects, if they have
a 'to_dict' method or an '__dict__' attribute.
"""


class SerializableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__({
            k: self.serialize(v) for k, v in dict(*args, **kwargs).items()
            if not (isinstance(k, str) and k.startswith('_'))
        })

    @classmethod
    def serialize(cls, o):
        if hasattr(o, "to_dict"):
            return cls.serialize(o.to_dict())
        if hasattr(o, "__dict__") and not isinstance(o, dict):
            return cls(o.__dict__)
        if isinstance(o, list):
            return [cls.serialize(item) for item in o]
        if isinstance(o, tuple):
            return tuple(cls.serialize(item) for item in o)
        if isinstance(o, dict):
            return cls(o)
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        if isinstance(o, decimal.Decimal):
            return str(o)
        return o


class CustomEncoder(_json.JSONEncoder):
    serializable_dict = SerializableDict

    def default(self, o):
        return self.serializable_dict.serialize(o)


class CustomJson:
    def __getattr__(self, attribute):
        return getattr(_json, attribute)

    def dumps(self, obj, *args, **kwargs):
        return _json.dumps(obj, cls=CustomEncoder, *args, **kwargs)


json = CustomJson()
