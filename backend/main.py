from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import Emission, Stamp, StampSeal, Sale, StampType
from backend.database import SessionLocal
from typing import List
from backend.schemas import EmissionCreate, EmissionResponse, StampCreate, StampResponse, StampSealBase, StampSealCreate, StampSealResponse, SaleCreate, SaleResponse, StampTypeCreate, StampTypeResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from backend import database_operations

app = FastAPI()

# ============================
# Middleware for connecting from web
# ============================
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================
# CRUD operations for Emission
# ============================
@app.post("/emissions/", response_model=EmissionResponse)
async def create_emission(emission_create: EmissionCreate, db: Session = Depends(get_db)):
    db_emission = Emission(**emission_create.model_dump())
    db.add(db_emission)
    db.commit()
    db.refresh(db_emission)
    return db_emission

@app.get("/emissions/", response_model=List[EmissionResponse])
async def read_emissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    emissions = db.query(Emission).offset(skip).limit(limit).all()
    return emissions

@app.get("/emissions/{emission_id}", response_model=EmissionResponse)
async def read_emission(emission_id: int, db: Session = Depends(get_db)):
    emission = db.query(Emission).filter(Emission.id == emission_id).first()
    if emission is None:
        raise HTTPException(status_code=404, detail="Emission not found")
    return emission

@app.put("/emissions/{emission_id}", response_model=EmissionResponse)
def update_emission(emission_id: int, updated_emission: EmissionCreate, db: Session = Depends(get_db)):
    existing_emission = db.query(Emission).filter(Emission.id == emission_id).first()
    if existing_emission is None:
        raise HTTPException(status_code=404, detail="Emission not found")
    
    for var, value in vars(updated_emission).items():
        setattr(existing_emission, var, value) if value else None

    db.commit()
    db.refresh(existing_emission)
    return existing_emission

@app.delete("/emissions/{emission_id}", response_model=EmissionResponse)
def delete_emission(emission_id: int, db: Session = Depends(get_db)):
    emission = db.query(Emission).filter(Emission.id == emission_id).first()
    if emission is None:
        raise HTTPException(status_code=404, detail="Emission not found")
    
    db.delete(emission)
    db.commit()
    return emission

# Endpoint pro získání emisí a příslušných známek
@app.get("/emissions-with-stamps/", response_model=list[EmissionResponse])
def get_emissions_with_stamps(db: Session = Depends(get_db)):
    emissions = db.query(Emission).all()
    emissions_with_stamps = []

    for emission in emissions:
        stamps = db.query(Stamp).filter(Stamp.emission_id == emission.id).all()
        emission_data = EmissionResponse(id=emission.id, name=emission.name, country=emission.country, description=emission.description, stamps=[StampResponse(id=stamp.id, catalog_number=stamp.catalog_number, name=stamp.name, emission_id=stamp.emission_id, country=stamp.country, photo_path_basic=stamp.photo_path_basic) for stamp in stamps])
        emissions_with_stamps.append(emission_data)

    return emissions_with_stamps

# ============================
# CRUD operations for Stamp
# ============================
@app.post("/stamps/", response_model=StampResponse)
def create_stamp(stamp_create: StampCreate, db: Session = Depends(get_db)):
    db_stamp = Stamp(**stamp_create.model_dump())
    db.add(db_stamp)
    db.commit()
    db.refresh(db_stamp)
    return db_stamp

@app.get("/stamps/", response_model=List[StampResponse])
def read_stamps(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    stamps = db.query(Stamp).offset(skip).limit(limit).all()
    return stamps

@app.get("/stamps/{stamp_id}", response_model=StampResponse)
def read_stamp(stamp_id: int, db: Session = Depends(get_db)):
    stamp = db.query(Stamp).filter(Stamp.id == stamp_id).first()
    if stamp is None:
        raise HTTPException(status_code=404, detail="Stamp not found")
    return stamp

@app.put("/stamps/{stamp_id}", response_model=StampResponse)
def update_stamp(stamp_id: int, updated_stamp: StampCreate, db: Session = Depends(get_db)):
    existing_stamp = db.query(Stamp).filter(Stamp.id == stamp_id).first()
    if existing_stamp is None:
        raise HTTPException(status_code=404, detail="Stamp not found")
    
    for var, value in vars(updated_stamp).items():
        setattr(existing_stamp, var, value) if value else None

    db.commit()
    db.refresh(existing_stamp)
    return existing_stamp

@app.delete("/stamps/{stamp_id}", response_model=StampResponse)
def delete_stamp(stamp_id: int, db: Session = Depends(get_db)):
    stamp = db.query(Stamp).filter(Stamp.id == stamp_id).first()
    if stamp is None:
        raise HTTPException(status_code=404, detail="Stamp not found")
    
    db.delete(stamp)
    db.commit()
    return stamp

# ============================
# CRUD operations for Stamp + StampType
# ============================

@app.get("/stamp/{stamp_id}/types/")
def get_stamp_types(stamp_id: int, db: Session = Depends(get_db)):
    return database_operations.get_stamp_types(db, stamp_id)

# Stamp + StampType + Sale
@app.get("/stamp/{stamp_id}/types/sale")
def get_stamp_types(stamp_id: int, db: Session = Depends(get_db)):
    return database_operations.get_stamp_type_and_price(db, stamp_id)

# ============================
# CRUD operations for StampType
# ============================
@app.post("/stamp-types/", response_model=StampTypeResponse)
def create_stamp_type(stamp_type_create: StampTypeCreate, db: Session = Depends(get_db)):
    db_stamp_type = StampType(**stamp_type_create.dict())
    db.add(db_stamp_type)
    db.commit()
    db.refresh(db_stamp_type)
    return db_stamp_type

@app.get("/stamp-types/{stamp_type_id}/", response_model=StampTypeResponse)
def get_stamp_type(stamp_type_id: int, db: Session = Depends(get_db)):
    db_stamp_type = db.query(StampType).filter(StampType.id == stamp_type_id).first()
    if db_stamp_type is None:
        raise HTTPException(status_code=404, detail="Stamp Type not found")
    return db_stamp_type

@app.put("/stamp-types/{stamp_type_id}/", response_model=StampTypeResponse)
def update_stamp_type(stamp_type_id: int, stamp_type_update: StampTypeCreate, db: Session = Depends(get_db)):
    db_stamp_type = db.query(StampType).filter(StampType.id == stamp_type_id).first()
    if db_stamp_type is None:
        raise HTTPException(status_code=404, detail="Stamp Type not found")
    
    for key, value in stamp_type_update.model_dump().items():
        setattr(db_stamp_type, key, value)

    db.commit()
    db.refresh(db_stamp_type)
    return db_stamp_type

@app.delete("/stamp-types/{stamp_type_id}/", response_model=StampTypeResponse)
def delete_stamp_type(stamp_type_id: int, db: Session = Depends(get_db)):
    db_stamp_type = db.query(StampType).filter(StampType.id == stamp_type_id).first()
    if db_stamp_type is None:
        raise HTTPException(status_code=404, detail="Stamp Type not found")

    db.delete(db_stamp_type)
    db.commit()

    return db_stamp_type

# ============================
# CRUD operations for StampSeal
# ============================
@app.post("/stampseals/", response_model=StampSealResponse)
def create_stamp_seal(stamp_seal_create: StampSealCreate, db: Session = Depends(get_db)):
    db_stamp_seal = StampSeal(**stamp_seal_create.dict())
    db.add(db_stamp_seal)
    db.commit()
    db.refresh(db_stamp_seal)
    return db_stamp_seal

@app.get("/stampseals/", response_model=List[StampSealResponse])
def read_stamp_seals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    stamp_seals = db.query(StampSeal).offset(skip).limit(limit).all()
    return stamp_seals

@app.get("/stampseals/{stamp_seal_id}", response_model=StampSealResponse)
def read_stamp_seal(stamp_seal_id: int, db: Session = Depends(get_db)):
    stamp_seal = db.query(StampSeal).filter(StampSeal.id == stamp_seal_id).first()
    if stamp_seal is None:
        raise HTTPException(status_code=404, detail="StampSeal not found")
    return stamp_seal

@app.put("/stampseals/{stamp_seal_id}", response_model=StampSealResponse)
def update_stamp_seal(stamp_seal_id: int, updated_stamp_seal: StampSealCreate, db: Session = Depends(get_db)):
    existing_stamp_seal = db.query(StampSeal).filter(StampSeal.id == stamp_seal_id).first()
    if existing_stamp_seal is None:
        raise HTTPException(status_code=404, detail="StampSeal not found")
    
    for var, value in vars(updated_stamp_seal).items():
        setattr(existing_stamp_seal, var, value) if value else None

    db.commit()
    db.refresh(existing_stamp_seal)
    return existing_stamp_seal

@app.delete("/stampseals/{stamp_seal_id}", response_model=StampSealResponse)
def delete_stamp_seal(stamp_seal_id: int, db: Session = Depends(get_db)):
    stamp_seal = db.query(StampSeal).filter(StampSeal.id == stamp_seal_id).first()
    if stamp_seal is None:
        raise HTTPException(status_code=404, detail="StampSeal not found")
    
    db.delete(stamp_seal)
    db.commit()
    return stamp_seal

# ============================
# CRUD operations for Sale
# ============================
@app.post("/sales/", response_model=SaleResponse)
def create_sale(sale_create: SaleCreate, db: Session = Depends(get_db)):
    db_sale = Sale(**sale_create.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@app.get("/sales/", response_model=List[SaleResponse])
def read_sales(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    sales = db.query(Sale).offset(skip).limit(limit).all()
    return sales

@app.get("/sales/{sale_id}", response_model=SaleResponse)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@app.put("/sales/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id: int, updated_sale: SaleCreate, db: Session = Depends(get_db)):
    existing_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if existing_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    for var, value in vars(updated_sale).items():
        setattr(existing_sale, var, value) if value else None

    db.commit()
    db.refresh(existing_sale)
    return existing_sale

@app.delete("/sales/{sale_id}", response_model=SaleResponse)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    db.delete(sale)
    db.commit()
    return sale


# ===================================
# Swagger
# ===================================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Your API description",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
