from datetime import datetime, timezone
from enum import Enum

class AbbreviatedEnum(Enum):
    def __str__(self) -> str:
        default = super().__str__()
        start = default.find(self.name)
        return default[start:].lower()

class AdvancedEnum(Enum):
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

class SerializableTime(datetime):
    def __str__(self) -> str:
        prev = self.tzinfo
        self.replace(tzinfo=timezone.utc)
        utc = self.timestamp()
        self.replace(tzinfo=prev)
        return str(utc)

    def __repr__(self) -> str:
        return self.__str__()

class PublicOnlyDict:
    def GetDict(self):
        public = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                public[k] = v
        return public