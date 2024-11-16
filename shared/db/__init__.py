import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from .models import Base

# Načítání proměnných z .env
load_dotenv()

# Nastavení připojení k SQLite databázi
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///stamps.db')
engine = create_engine(DATABASE_URL, echo=True)

# Vytvoření tabulek podle definovaných modelů
Base.metadata.create_all(engine)

# Vytvoření session pro práci s databází
Session = sessionmaker(bind=engine)
session = Session()