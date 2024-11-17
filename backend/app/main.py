from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from shared.db import crud
from pydantic import BaseModel
from typing import List




app = FastAPI()

templates = Jinja2Templates(directory="backend/templates")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Pydantic model pro emisii
class EmissionCreate(BaseModel):
    name: str
    country: str
    issue_year: int

class EmissionResponse(EmissionCreate):
    emission_id: int

    class Config:
        from_attributes = True

# Pydantic model pro známku
class StampCreate(BaseModel):
    catalog_number: str
    photo_path_base: str
    emission_id: int

class StampResponse(StampCreate):
    stamp_id: int

    class Config:
        from_attributes = True

# Pydantic model pro zemi
class CountryCreate(BaseModel):
    name: str

class CountryResponse(CountryCreate):
    country_id: int

    class Config:
        from_attributes = True

# APi Endpoint with html poge
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Katalog známek
@app.get("/catalog", response_class=HTMLResponse)
def catalog(request: Request, country: str = None):
    countries = crud.get_all_countries()  # Získání seznamu zemí z databáze
    emissions = []
    if country:
        emissions = crud.get_emissions_by_country(country)  # Filtr podle země
    return templates.TemplateResponse(
        "catalog.html",
        {"request": request, "countries": countries, "emissions": emissions, "selected_country": country},
    )

# Endpoint for bootstrap or for working with data
# Endpoint pro přidání emise
@app.post("/emissions/", response_model=EmissionResponse)
def create_emission(emission: EmissionCreate):
    country = crud.get_country_by_name(emission.country)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return crud.insert_emission(emission.name, country, emission.issue_year)

# Endpoint pro získání všech emisí
@app.get("/emissions/", response_model=List[EmissionResponse])
def get_emissions():
    return crud.get_all_emissions()

# Endpoint pro získání emise podle ID
@app.get("/emissions/{emission_id}", response_model=EmissionResponse)
def get_emission(emission_id: int):
    emission = crud.get_emission_by_id(emission_id)
    if not emission:
        raise HTTPException(status_code=404, detail="Emission not found")
    return emission

# Endpoint pro přidání známky
@app.post("/stamps/", response_model=StampResponse)
def create_stamp(stamp: StampCreate):
    return crud.insert_stamp(stamp.catalog_number, stamp.photo_path_base, stamp.emission_id)

# Endpoint pro získání všech známek
@app.get("/stamps/", response_model=List[StampResponse])
def get_stamps():
    return crud.get_all_stamps()

# Endpoint pro získání známky podle ID
@app.get("/stamps/{stamp_id}", response_model=StampResponse)
def get_stamp(stamp_id: int):
    stamp = crud.get_stamp_by_id(stamp_id)
    if not stamp:
        raise HTTPException(status_code=404, detail="Stamp not found")
    return stamp

# Endpoint pro přidání země
@app.post("/countries/", response_model=CountryResponse)
def create_country(country: CountryCreate):
    return crud.insert_country(country.name)

# Endpoint pro získání všech zemí
@app.get("/countries/", response_model=List[CountryResponse])
def get_countries():
    return crud.get_all_countries()

# Endpoint pro získání země podle ID
@app.get("/countries/{country_id}", response_model=CountryResponse)
def get_country(country_id: int):
    country = crud.get_country_by_id(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

# Endpoint pro získání všech známek podle země
@app.get("/stamps/country/{country_name}", response_model=List[StampResponse])
def get_stamps_by_country(country_name: str):
    stamps = crud.get_stamps_by_country(country_name)
    if not stamps:
        raise HTTPException(status_code=404, detail="No stamps found for this country")
    return stamps

# Endpoint pro získání všech známek podle emise
@app.get("/stamps/emission/{emission_name}", response_model=List[StampResponse])
def get_stamps_by_emission(emission_name: str):
    stamps = crud.get_stamps_by_emission(emission_name)
    if not stamps:
        raise HTTPException(status_code=404, detail="No stamps found for this emission")
    return stamps
