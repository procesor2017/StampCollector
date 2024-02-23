from sqlalchemy import create_engine
from models import Base

# Konfigurace databázového připojení
DATABASE_URL = "sqlite:///./data/test.db"
engine = create_engine(DATABASE_URL)

# Vytvoření tabulek v databázi
Base.metadata.create_all(bind=engine)