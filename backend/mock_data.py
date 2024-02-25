import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Emission, Base, Stamp, StampType

def create_tables(engine):
    Base.metadata.create_all(bind=engine)

def fill_emissions(session):
    emissions_data = [
        {"name": "Emission 1", "country": "o-u"},
        {"name": "Emission 2", "country": "cs"},
    ]

    for data in emissions_data:
        emission = Emission(**data)
        session.add(emission)

    session.commit()

def fill_stamps(session):
    stamps_data = [
        {"catalog_number": 1, "emission_id": 1, "name": "I. Kr", "country": "o-u", "photo_path_basic": ""},
        {"catalog_number": 2, "emission_id": 1, "name": "II. Kr", "country": "o-u", "photo_path_basic": ""},
        {"catalog_number": 3, "emission_id": 2, "name": "200h", "country": "cs", "photo_path_basic": ""},
    ]

    for data in stamps_data:
        stamp = Stamp(**data)
        session.add(stamp)

    session.commit()

def fill_stamp_types(session):
    stamp_types_data = [
        {"stamp_id": 1, "photo_path_type": "path_type1", "description": "Desc 1", "type": "Type 1", "color": "Color 1", "quality": "Good", "perforation": "Perforation 1", "plate_flaw": 1, "catalog_price": 10.5},
        {"stamp_id": 1, "photo_path_type": "path_type2", "description": "Desc 2", "type": "Type 2", "color": "Color 2", "quality": "Excellent", "perforation": "Perforation 2", "plate_flaw": 0, "catalog_price": 15.0},
        {"stamp_id": 1, "photo_path_type": "path_type3", "description": "Desc 3", "type": "Type 3", "color": "Color 3", "quality": "Good", "perforation": "Perforation 3", "plate_flaw": 2, "catalog_price": 12.0},
        {"stamp_id": 2, "photo_path_type": "path_type4", "description": "Desc 4", "type": "Type 4", "color": "Color 4", "quality": "Excellent", "perforation": "Perforation 4", "plate_flaw": 0, "catalog_price": 20.0},
        {"stamp_id": 3, "photo_path_type": "path_type5", "description": "Desc 5", "type": "Type 5", "color": "Color 5", "quality": "Good", "perforation": "Perforation 5", "plate_flaw": 1, "catalog_price": 18.0},
    ]

    for data in stamp_types_data:
        stamp_type = StampType(**data)
        session.add(stamp_type)

    session.commit()

if __name__ == "__main__":
    engine = create_engine('sqlite:///./data/test.db', echo=True)

    # Vytvoření tabulek, pokud neexistují
    create_tables(engine)

    # Vytvoření relace a naplnění daty
    with Session(engine) as session:
        fill_emissions(session)
        fill_stamps(session)
        fill_stamp_types(session)
