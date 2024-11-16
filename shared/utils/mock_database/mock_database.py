import pandas as pd
from sqlalchemy.orm import sessionmaker
from shared.db.models import Country, Emission, StampBase, StampTypeBase
from shared.db import engine

Session = sessionmaker(bind=engine)
session = Session()

# Funkce pro vložení dat do tabulek
def insert_data_from_df(df, model_class):
    for index, row in df.iterrows():
        data_instance = model_class(**row.to_dict())
        session.add(data_instance)
    session.commit()


def insert_emission_data(df):
    for _, row in df.iterrows():
        country = session.query(Country).filter(Country.country_id == row['country_id']).first()
        if country:
            emission = Emission(
                name=row['name'],
                issue_year=row['issue_year'],
                country_id=country.country_id
            )
            session.add(emission)
    session.commit()

def insert_stamp_data(df):
    for _, row in df.iterrows():
        emission = session.query(Emission).filter(Emission.emission_id == row['emission_id']).first()
        if emission:
            stamp = StampBase(
                catalog_number=row['catalog_number'],
                photo_path_base=row['photo_path_base'],
                name=row['name'],
                emission_id=emission.emission_id
            )
            session.add(stamp)
    session.commit()

def insert_stamp_type_data(df):
    for _, row in df.iterrows():
        stamp = session.query(StampBase).filter(StampBase.stamp_id == row['stamp_id']).first()
        if stamp:
            stamp_type = StampTypeBase(
                stamp_id=stamp.stamp_id,
                photo_path_type=row['photo_path_type'],
                description=row['description'],
                type_name=row['type_name'],
                color=row['color'],
                paper=row['paper'],
                perforation=row['perforation'],
                plate_flaw=row['plate_flaw'],
                catalog_price_superb=row['catalog_price_superb'],
                catalog_price_extra_fine=row['catalog_price_extra_fine'],
                catalog_price_very_fine=row['catalog_price_very_fine'],
                catalog_price_fine=row['catalog_price_fine'],
                catalog_price_avg=row['catalog_price_avg'],
                catalog_price_poor=row['catalog_price_poor'],
                catalog_price_post_cover=row['catalog_price_post_cover']
            )
            session.add(stamp_type)
    session.commit()

# Načítáme data z CSV souborů
country_df = pd.read_csv('data/csv/country.csv')
emission_df = pd.read_csv('data/csv/emission.csv')
stamp_type_df = pd.read_csv('data/csv/stamp_type.csv')
stamp_base_df = pd.read_csv('data/csv/stampBase.csv')

# Vkládáme data do databáze s relacemi
insert_emission_data(emission_df)
insert_stamp_data(stamp_base_df)
insert_stamp_type_data(stamp_type_df)

session.close()