from datetime import datetime, timezone

def NotEmpty(x):
    return x is not None and x != ''

class SerializableTime(datetime):
    def __str__(self) -> str:
        prev = self.tzinfo
        self.replace(tzinfo=timezone.utc)
        utc = self.timestamp()
        self.replace(tzinfo=prev)
        return str(utc)

    def __repr__(self) -> str:
        return self.__str__()