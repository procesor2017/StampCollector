from fastapi import FastAPI, HTTPException, Request, Depends
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from shared.db import crud
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import RedirectResponse
from shared.db.database import initialize_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database when the app starts
    await initialize_db()
    yield

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="backend/templates")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")
app.mount("/images", StaticFiles(directory="data/images"), name="images")


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

class StampTypeBaseResponse(BaseModel):
    stamp_type_id: int
    photo_path_type: Optional[str]
    description: Optional[str]
    type_name: Optional[str]
    color: Optional[str]
    paper: Optional[str]
    perforation: Optional[str]
    plate_flaw: Optional[str]
    catalog_price_superb: Optional[float]
    catalog_price_extra_fine: Optional[float]
    catalog_price_very_fine: Optional[float]
    catalog_price_fine: Optional[float]
    catalog_price_avg: Optional[float]
    catalog_price_poor: Optional[float]
    catalog_price_post_cover: Optional[float]

    class Config:
        from_attributes = True

class AuctionSale(BaseModel):
    stamp_type_id: int
    sale_price: int
    sale_url: str
    description: str

class StampBaseResponse(BaseModel):
    stamp_id: int
    catalog_number: str
    photo_path_base: str
    name: str
    emission_id: int  # pokud chcete zahrnout i emisní ID
    stamp_types: List[StampTypeBaseResponse]  # Podtypy známek

    class Config:
        from_attributes = True

# APi Endpoint with html poge
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Katalog známek
@app.get("/catalog/{country}", response_class=HTMLResponse, name="catalog")
@app.get("/catalog", response_class=HTMLResponse, name="catalog_no_country")
def catalog(request: Request, country: str = None):
    countries = crud.get_all_countries()  # Seznam všech zemí
    if country:
        emissions = crud.get_emissions_by_country(country)  # Filtr podle země
    else:
        emissions = crud.get_emissions_by_country(None)  # Pokud není země, nezobrazovat filtr
    return templates.TemplateResponse(
        "catalog.html",
        {"request": request, "countries": countries, "emissions": emissions, "selected_country": country},
    )

# Detail emise
@app.get("/emissions/{emission_id}", response_class=HTMLResponse)
async def emission_detail(request: Request, emission_id: int):
    # Získání emise podle ID
    emission = crud.get_emission_by_id(emission_id)
    if not emission:
        raise HTTPException(status_code=404, detail="Emission not found")
    
    # Získání všech známek pro tuto emisi
    stamps = crud.get_stamps_by_emission(emission.name)
    
    # Renderování detailu emise s listem známek
    return templates.TemplateResponse("emission_detail.html", {
        "request": request,
        "emission": emission,
        "stamps": stamps
    })

# Detail pro známku
@app.get("/stamps/{stamp_id}", response_class=HTMLResponse, name="stamp_detail")
async def get_stamp_detail(request: Request, stamp_id: int):
    # Získání detailu známky
    stamp = crud.get_stamp_by_id(stamp_id)
    if not stamp:
        raise HTTPException(status_code=404, detail="Stamp not found")

    # Získání podtypů pro známku
    subtypes = crud.get_all_stamp_type_by_id(stamp_id)

    # Získání aukcí pro každý podtyp známky
    auctions_by_subtype = {
        subtype.stamp_type_id: crud.get_auctions_by_stamp_type(subtype.stamp_type_id)
        for subtype in subtypes
    }

    return templates.TemplateResponse("stamp_detail.html", {
        "request": request,
        "stamp": stamp,
        "subtypes": subtypes,
        "auctions_by_subtype": auctions_by_subtype
    })

@app.get("/search", response_class=HTMLResponse, name="search_results")
def search_results(request: Request, query: str):
    # Vyhledání známek podle názvu
    stamps = crud.search_stamps_by_name(query)  # Implementace této metody je nutná
    if len(stamps) == 1:
        # Pokud je nalezena pouze jedna známka, přesměrovat přímo na její detail
        return RedirectResponse(url=f"/stamps/{stamps[0].stamp_id}")
    return templates.TemplateResponse(
        "search_results.html",
        {"request": request, "stamps": stamps, "query": query},
    )

# Endpoint for bootstrap or for working with data
# Endpoint pro přidání emise
@app.post("/api/emissions/", response_model=EmissionResponse)
def create_emission(emission: EmissionCreate):
    country = crud.get_country_by_name(emission.country)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return crud.insert_emission(emission.name, country, emission.issue_year)

# Endpoint pro získání všech emisí
@app.get("/api/emissions/", response_model=List[EmissionResponse])
def get_emissions():
    return crud.get_all_emissions()

# Endpoint pro získání emise podle ID
@app.get("/api/emissions/{emission_id}", response_model=EmissionResponse)
def get_emission(emission_id: int):
    emission = crud.get_emission_by_id(emission_id)
    if not emission:
        raise HTTPException(status_code=404, detail="Emission not found")
    return emission

# Endpoint pro přidání známky
@app.post("/api/stamps/", response_model=StampResponse)
def create_stamp(stamp: StampCreate):
    return crud.insert_stamp(stamp.catalog_number, stamp.photo_path_base, stamp.emission_id)

# Endpoint pro získání všech známek
@app.get("/api/stamps/", response_model=List[StampResponse])
def get_stamps():
    return crud.get_all_stamps()

# Endpoint pro získání známky podle ID
@app.get("/api/stamps/{stamp_id}", response_model=StampResponse)
def get_stamp(stamp_id: int):
    stamp = crud.get_stamp_by_id(stamp_id)
    if not stamp:
        raise HTTPException(status_code=404, detail="Stamp not found")
    return stamp

# Endpoint pro přidání země
@app.post("/api/countries/", response_model=CountryResponse)
def create_country(country: CountryCreate):
    return crud.insert_country(country.name)

# Endpoint pro získání všech zemí
@app.get("/api/countries/", response_model=List[CountryResponse])
def get_countries():
    return crud.get_all_countries()

# Endpoint pro získání země podle ID
@app.get("/api/countries/{country_id}", response_model=CountryResponse)
def get_country(country_id: int):
    country = crud.get_country_by_id(country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

# Endpoint pro získání všech známek podle země
@app.get("/api/stamps/country/{country_name}", response_model=List[StampResponse])
def get_stamps_by_country(country_name: str):
    stamps = crud.get_stamps_by_country(country_name)
    if not stamps:
        raise HTTPException(status_code=404, detail="No stamps found for this country")
    return stamps

# Endpoint pro získání všech známek podle emise
@app.get("/api/stamps/emission/{emission_name}", response_model=List[StampResponse])
def get_stamps_by_emission(emission_name: str):
    stamps = crud.get_stamps_by_emission(emission_name)
    if not stamps:
        raise HTTPException(status_code=404, detail="No stamps found for this emission")
    return stamps

@app.get("api/stamps/{stamp_id}", response_model=StampBaseResponse)
def get_stamp_detail(stamp_id: int):
    stamp = crud.get_stamp_by_id(stamp_id)
    if not stamp:
        raise HTTPException(status_code=404, detail="Stamp not found")
    
    # Získání podtypů
    subtypes = crud.get_all_stamp_type_by_id(stamp_id)
    
    # Převod SQLAlchemy objektů na Pydantic modely
    return StampBaseResponse(
        stamp_id=stamp.stamp_id,
        catalog_number=stamp.catalog_number,
        photo_path_base=stamp.photo_path_base,
        name=stamp.name,
        emission_id=stamp.emission_id,
        stamp_types=[StampTypeBaseResponse(**subtype.as_dict()) for subtype in subtypes]
    )

@app.post("/api/auctions")
def create_auction(stamp_type_id: int, price: float, url: str, description: str):
    auction = crud.add_auction(stamp_type_id, price, url, description)
    return {"message": "Auction added", "auction": auction}

@app.get("/api/auctions/{stamp_type_id}")
def get_auctions(stamp_type_id: int):
    auctions = crud.get_auctions_by_stamp_type(stamp_type_id)
    return {"auctions": auctions}
