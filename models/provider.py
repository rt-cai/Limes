from enum import Enum
from json.encoder import JSONEncoder
from typing import Tuple
from models.basic import AbbreviatedEnum, PublicOnlyDict

class Responsibility(AbbreviatedEnum):
    FASTA = 1

class RegistrationForm(PublicOnlyDict):
    def __init__(self, data: dict):
        self.Address = data['Address']
        # self.Responsibilities = data['responsibilities']
        

class RegistrationForm_Explicit(RegistrationForm):
    def __init__(self, address: str, responsibilities: list[Responsibility]) -> None:
        json = {
            'Address': address,
            'Responsibilities': responsibilities
        }
        super().__init__(json)