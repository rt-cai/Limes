from __future__ import annotations

from .. import config
from . import Model, provider as Models
from .provider import GenericResponse, Transaction, GenericRequest, Primitive
from .http import GET, PATCH, POST, PUT

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