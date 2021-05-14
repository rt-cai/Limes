from common.utils import SerializableTime


class Sample:
    def __init__(self, name: str = '') -> None:
        self.Name = name
        self.DateCreated = SerializableTime.now()
