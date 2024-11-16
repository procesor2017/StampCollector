from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from shared.db import crud, session as db_session
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Funkce pro získání session pro připojení k databázi
def get_db():
    db = db_session.Session()  # Používáme session z shared.db.session
    try:
        yield db
    finally:
        db.close()

# Pydantic model pro emisii
class EmissionCreate(BaseModel):
    name: str
    country: str
    issue_year: int

class EmissionResponse(EmissionCreate):
    emission_id: int

    class Config:
        orm_mode = True

# Pydantic model pro známku
class StampCreate(BaseModel):
    catalog_number: str
    photo_path_base: str
    emission_id: int

class StampResponse(StampCreate):
    stamp_id: int

    class Config:
        orm_mode = True

# Pydantic model pro zemi
class CountryCreate(BaseModel):
    name: str

class CountryResponse(CountryCreate):
    country_id: int

    class Config:
        orm_mode = True

# Endpoint pro přidání emise
@app.post("/emissions/", response_model=EmissionResponse)
def create_emission(emission: EmissionCreate, db: Session = Depends(get_db)):
    country = crud.get_country_by_name(emission.country, db)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return crud.insert_emission(emission.name, country, emission.issue_year, db)

# Endpoint pro získání všech emisí
@app.get("/emissions/", response_model=List[EmissionResponse])
def get_emissions(db: Session = Depends(get_db)):
    return crud.get_all_emissions(db)

# Endpoint pro získání emise podle ID
@app.get("/emissions/{emission_id}", response_model=EmissionResponse)
def get_emission(emission_id: int, db: Session = Depends(get_db)):
    emission = crud.get_emission_by_id(emission_id, db)
    if not emission:
        raise HTTPException(status_code=404, detail="Emission not found")
    return emission

# Endpoint pro přidání známky
@app.post("/stamps/", response_model=StampResponse)
def create_stamp(stamp: StampCreate, db: Session = Depends(get_db)):
    return crud.insert_stamp(stamp.catalog_number, stamp.photo_path_base, stamp.emission_id, db)

# Endpoint pro získání všech známek
@app.get("/stamps/", response_model=List[StampResponse])
def get_stamps(db: Session = Depends(get_db)):
    return crud.get_all_stamps(db)

# Endpoint pro získání známky podle ID
@app.get("/stamps/{stamp_id}", response_model=StampResponse)
def get_stamp(stamp_id: int, db: Session = Depends(get_db)):
    stamp = crud.get_stamp_by_id(stamp_id, db)
    if not stamp:
        raise HTTPException(status_code=404, detail="Stamp not found")
    return stamp

# Endpoint pro přidání země
@app.post("/countries/", response_model=CountryResponse)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    return crud.insert_country(country.name, db)

# Endpoint pro získání všech zemí
@app.get("/countries/", response_model=List[CountryResponse])
def get_countries(db: Session = Depends(get_db)):
    return crud.get_all_countries(db)

# Endpoint pro získání země podle ID
@app.get("/countries/{country_id}", response_model=CountryResponse)
def get_country(country_id: int, db: Session = Depends(get_db)):
    country = crud.get_country_by_id(country_id, db)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

# Endpoint pro získání všech známek podle země
@app.get("/stamps/country/{country_name}", response_model=List[StampResponse])
def get_stamps_by_country(country_name: str, db: Session = Depends(get_db)):
    stamps = crud.get_stamps_by_country(country_name, db)
    if not stamps:
        raise HTTPException(status_code=404, detail="No stamps found for this country")
    return stamps

# Endpoint pro získání všech známek podle emise
@app.get("/stamps/emission/{emission_name}", response_model=List[StampResponse])
def get_stamps_by_emission(emission_name: str, db: Session = Depends(get_db)):
    stamps = crud.get_stamps_by_emission(emission_name, db)
    if not stamps:
        raise HTTPException(status_code=404, detail="No stamps found for this emission")
    return stamps
