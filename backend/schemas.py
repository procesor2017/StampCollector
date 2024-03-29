from pydantic import BaseModel
from typing import List

# Schémata pro Stamp
class StampBase(BaseModel):
    catalog_number: int
    emission_id: int
    name: str
    country: str
    photo_path_basic: str

class StampCreate(StampBase):
    pass

class StampResponse(StampBase):
    id: int

# Schémata pro Emission
class EmissionBase(BaseModel):
    name: str
    country: str
    description: str

class EmissionCreate(EmissionBase):
    pass

class EmissionResponse(EmissionBase):
    id: int
    stamps: List[StampResponse]  = [] # Nepoviný arg

# Schémata pro StampType
class StampTypeBase(BaseModel):
    stamp_id: int
    photo_path_type: str
    description: str
    type: str
    color: str
    quality: str
    perforation: str
    plate_flaw: int
    catalog_price: float

class StampTypeCreate(StampTypeBase):
    pass

class StampTypeResponse(StampTypeBase):
    stamp_type_id: int

# Schémata pro StampSeal
class StampSealBase(BaseModel):
    stamp_type_id: int
    rating: int
    description: str
    photo: str

class StampSealCreate(StampSealBase):
    pass

class StampSealResponse(StampSealBase):
    id: int

# Schémata pro Sale
class SaleBase(BaseModel):
    stamp_type_id: int
    price: float
    sale_date: str
    name_of_auction: str
    url_on_auction: str
    description: str
    strip: bool
    convolut: bool

class SaleCreate(SaleBase):
    pass

class SaleResponse(SaleBase):
    id: int
