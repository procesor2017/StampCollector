import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from shared.db.models import Country, Emission, StampBase, StampTypeBase
from shared.db import engine

# Nastavení session
Session = sessionmaker(bind=engine)
session = Session()

# Funkce pro vložení dat do tabulek
def insert_data_with_commit(df, model_class):
    try:
        for index, row in df.iterrows():
            print(f"Inserting into {model_class.__name__}: {row.to_dict()}")
            data_instance = model_class(**row.to_dict())
            session.add(data_instance)
        session.commit()
        print(f"Data successfully committed to {model_class.__name__}")
    except SQLAlchemyError as e:
        print(f"Error inserting into {model_class.__name__}: {e}")
        session.rollback()

def insert_emission_data(df):
    try:
        for _, row in df.iterrows():
            country = session.query(Country).filter(Country.country_id == row['country_id']).first()
            if country:
                print(f"Inserting emission: {row['name']}, year: {row['issue_year']}, country_id: {country.country_id}")
                emission = Emission(
                    name=row['name'],
                    issue_year=row['issue_year'],
                    country_id=country.country_id
                )
                session.add(emission)
        session.commit()
        print("Emissions successfully committed.")
    except SQLAlchemyError as e:
        print(f"Error inserting emissions: {e}")
        session.rollback()

def insert_stamp_data(df):
    try:
        for index, row in df.iterrows():
            emission = session.query(Emission).filter(Emission.emission_id == row['emission_id']).first()
            if emission:
                # Pokud je hodnota 'None', nastavte ji na nějakou výchozí hodnotu
                photo_path_base = row['photo_path_base'] if pd.notna(row['photo_path_base']) else 'unknown'
                stamp = StampBase(
                    catalog_number=row['catalog_number'],
                    photo_path_base=photo_path_base,  # Nastaví se výchozí hodnota, pokud je None
                    name=row['name'],
                    emission_id=emission.emission_id
                )
                session.add(stamp)
                print(f"Inserting stamp: {row['name']}, catalog_number: {row['catalog_number']}, emission_id: {emission.emission_id}")
        session.commit()
    except Exception as e:
        print(f"Error inserting stamps: {e}")
        session.rollback()

def insert_stamp_type_data(df):
    try:
        for index, row in df.iterrows():
            stamp = session.query(StampBase).filter(StampBase.stamp_id == row['stamp_id']).first()
            if stamp:
                # Pokud je hodnota 'None', nastavte ji na nějakou výchozí hodnotu
                photo_path_type = row['photo_path_type'] if pd.notna(row['photo_path_type']) else 'unknown'
                stamp_type = StampTypeBase(
                    stamp_id=stamp.stamp_id,
                    photo_path_type=photo_path_type,  # Nastaví se výchozí hodnota, pokud je None
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
                print(f"Inserting stamp type: {row['type_name']}, stamp_id: {stamp.stamp_id}")
        session.commit()
    except Exception as e:
        print(f"Error inserting stamp types: {e}")
        session.rollback()



# Načítání dat z CSV souborů
try:
    country_df = pd.read_csv('data/csv/country.csv')
    emission_df = pd.read_csv('data/csv/emission.csv')
    stamp_base_df = pd.read_csv('data/csv/stampBase.csv')
    stamp_type_df = pd.read_csv('data/csv/stamp_type.csv')


    print("CSV files loaded successfully.")
    print(country_df.head())
    print(emission_df.head())
    print(stamp_type_df.head())
    print(stamp_base_df.head())
except Exception as e:
    print(f"Error loading CSV files: {e}")

# Vkládání dat do databáze s relacemi
try:
    insert_data_with_commit(country_df, Country)
    insert_emission_data(emission_df)
    insert_stamp_data(stamp_base_df)
    insert_stamp_type_data(stamp_type_df)
except Exception as e:
    print(f"Unexpected error during data insertion: {e}")
finally:
    session.close()
    print("Session closed.")
