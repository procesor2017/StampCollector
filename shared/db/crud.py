from . import session
from .models import Emission, StampBase, StampTypeBase, Country, AuctionSale

# Emissions
def insert_emission(name, country, issue_year):
    new_emission = Emission(name=name, country=country, issue_year=issue_year)
    session.add(new_emission)
    session.commit()
    return new_emission

def get_all_emissions():
    return session.query(Emission).all()

def get_emission_by_id(emission_id):
    return session.query(Emission).filter(Emission.emission_id == emission_id).first()

def get_emissions_by_country(country):
    country_id = get_country_by_name_and_return_id(country)
    return session.query(Emission).filter(Emission.country_id == country_id).all()

# Stamps
# Basic Stamps
def insert_stamp(catalog_number, photo_path_base, emission_id):
    new_stamp = StampBase(catalog_number=catalog_number, photo_path_base=photo_path_base, emission_id=emission_id)
    session.add(new_stamp)
    session.commit()
    return new_stamp

def get_all_stamps():
    return session.query(StampBase).all()

def get_stamp_by_id(stamp_id):
    return session.query(StampBase).filter(StampBase.stamp_id == stamp_id).first()

#Stamps Type
def insert_stamp_type(stamp_id, photo_path_type, description, type_name, color, paper, perforation, plate_flaw):
    new_stamp_type = StampTypeBase(
        stamp_id=stamp_id,
        photo_path_type=photo_path_type,
        description=description,
        type_name=type_name,
        color=color,
        paper=paper,
        perforation=perforation,
        plate_flaw=plate_flaw
    )
    session.add(new_stamp_type)
    session.commit()
    return new_stamp_type

def get_all_stamp_types():
    return session.query(StampTypeBase).all()

def get_stamp_type_by_id(stamp_id):
    return session.query(StampTypeBase).filter(StampTypeBase.stamp_id == stamp_id).first()

def get_all_stamp_type_by_id(stamp_id):
    return session.query(StampTypeBase).filter(StampTypeBase.stamp_id == stamp_id).all()

# Country
def insert_country(name):
    new_country = Country(name=name)
    session.add(new_country)
    session.commit()
    return new_country

def get_all_countries():
    return session.query(Country).all()

def get_country_by_id(country_id):
    return session.query(Country).filter(Country.country_id == country_id).first()

def get_country_by_name(name):
    return session.query(Country).filter(Country.name == name).first()

def get_country_by_name_and_return_id(name):
    result = session.query(Country.country_id).filter(Country.name == name).first()
    if result:
        return result[0]  # vrací první (a jediné) pole, což je `country_id`
    return None

# Stamps via country Name
def get_stamps_by_country(country_name):
    country = session.query(Country).filter(Country.name == country_name).first()
    if country:
        emissions = session.query(Emission).filter(Emission.country_id == country.country_id).all()
        stamps = []
        for emission in emissions:
            stamps.extend(session.query(StampBase).filter(StampBase.emission_id == emission.emission_id).all())
        return stamps
    return []

# Stmaps via emission
def get_stamps_by_emission(emission_name):
    emission = session.query(Emission).filter(Emission.name == emission_name).first()
    if emission:
        return session.query(StampBase).filter(StampBase.emission_id == emission.emission_id).all()
    return []

def search_stamps_by_name(query: str):
    return (
        session.query(StampBase)
        .filter(StampBase.name.ilike(f"%{query}%"))
        .all()
    )

# Přidání nové aukce
def add_auction(stamp_type_id: int, price: float, url: str, description: str):
    auction = AuctionSale(
        stamp_type_id=stamp_type_id,
        price=price,
        url=url,
        description=description
    )
    session.add(auction)
    session.commit()
    return auction

# Získání všech aukcí pro daný typ známky
def get_auctions_by_stamp_type(stamp_type_id: int):
    return session.query(AuctionSale).filter(AuctionSale.stamp_type_id == stamp_type_id).all()