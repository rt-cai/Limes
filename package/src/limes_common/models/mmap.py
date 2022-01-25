from __future__ import annotations

from limes_common import config
from limes_common.models import Model, provider as Models
from limes_common.models.provider import GenericResponse, Transaction, GenericRequest, Primitive
from limes_common.models.http import GET, PATCH, POST, PUT

class Endpoints(Models.Endpoints):
    SequencingFacilityQuery = 'SequencingFacilityQuery'


class SequencingFacilityQuery(Transaction):
    class Request(GenericRequest):
        status: str
        barcode: str

        def __init__(self) -> None:
            super().__init__(Endpoints.SequencingFacilityQuery, POST)

    class Response(GenericResponse):
        pass