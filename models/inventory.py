from common.utils import SerializableTime
from common.config import ActiveGeneric as Config

class Sample:
    def __init__(self, data: dict, timeFormat: str) -> None:
        self._id = data['sampleID']
        self._storageLayerId = data['storageLayerID']
        self._position = data['position']
        self._barcode = data['barcode']
        self._typeId = data['sampleTypeID']
        self._parentSampleId = data['parentSampleID']
        self._raw = data if Config.KEEP_RAW_DATA else None

        self.Name = data['name']
        self.Owner = data['owner']
        self.DateCreated = SerializableTime.strptime(data['created'], timeFormat)
        self.Description = data['description']
        self.Note = data['note']

    def __str__(self):
        public = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                public[k] = v
        return str(public)
