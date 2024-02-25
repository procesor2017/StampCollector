import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Emission, Base, Stamp, StampType

def create_tables(engine):
    Base.metadata.create_all(bind=engine)

def fill_emissions_from_csv(session, csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name, country, description = row
            emission = Emission(name=name, country=country, description=description)
            session.add(emission)

        session.commit()

def fill_stamps_from_csv(session, csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            catalog_number, emission_id, name, country, photo_path_basic = row
            catalog_number, emission_id = map(int, (catalog_number, emission_id))

            stamp = Stamp(
                catalog_number=str(catalog_number),
                emission_id=emission_id,
                name=name.strip(),
                country=country,
                photo_path_basic=photo_path_basic
            )
            session.add(stamp)

        session.commit()


def fill_stamp_types_from_csv(session, csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            (
                stamp_id, photo_path_type, description, type_name, color,
                quality, perforation, plate_flaw, catalog_price
            ) = row
            stamp_type_instance = StampType(
                stamp_id=stamp_id,
                photo_path_type=photo_path_type,
                description=description,
                type=type_name,
                color=color,
                quality=quality,
                perforation=perforation,
                plate_flaw=plate_flaw,
                catalog_price=catalog_price
            )
            session.add(stamp_type_instance)

        session.commit()


if __name__ == "__main__":
    engine = create_engine('sqlite:///./data/test.db', echo=True)

    # Vytvoření tabulek, pokud neexistují
    create_tables(engine)

    # Vytvoření relace a naplnění daty z CSV
    with Session(engine) as session:
        fill_emissions_from_csv(session, 'data/csv/emissions.csv')
        fill_stamps_from_csv(session, 'data/csv/stamps.csv')
        fill_stamp_types_from_csv(session, 'data/csv/stamps_type.csv')
