# shared/db/crud.py
from . import session
from .models import Emission, StampBase, StampTypeBase

# Funkce pro přidání emise
def insert_emission(name, country, issue_year):
    new_emission = Emission(name=name, country=country, issue_year=issue_year)
    session.add(new_emission)
    session.commit()

# Funkce pro přidání známky
def insert_stamp(catalog_number, photo_path_base, emission_id):
    new_stamp = StampBase(catalog_number=catalog_number, photo_path_base=photo_path_base, emission_id=emission_id)
    session.add(new_stamp)
    session.commit()
