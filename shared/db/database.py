import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .models import Base


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)

def initialize_db():
    # Kontrola, zda databázový soubor existuje
    if not os.path.exists(DATABASE_URL.split('///')[1]):
        print("Databáze neexistuje, vytvářím ji...")
        # Pokud databáze neexistuje, vytvoříme ji a tabulky
        Base.metadata.create_all(engine)
        print("Databáze a tabulky byly úspěšně vytvořeny.")
    else:
        print("Databáze již existuje, tabulky jsou připravené.")
