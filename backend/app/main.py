from fastapi import FastAPI
from shared.db.crud import insert_emission, insert_stamp
from shared.db import database
from contextlib import asynccontextmanager

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run startup logic
    print("Starting application...")
    database.initialize_db()  # Initialize the DB when the app starts up
    yield  # This allows FastAPI to run the app's normal event loop
    # Run shutdown logic if needed
    print("Shutting down application...")

@app.get("/add_emission")
def add_emission(name: str, country: str, issue_year: int):
    insert_emission(name, country, issue_year)
    return {"message": "Emission added successfully"}

@app.get("/add_stamp")
def add_stamp(catalog_number: str, photo_path_base: str, emission_id: int):
    insert_stamp(catalog_number, photo_path_base, emission_id)
    return {"message": "Stamp added successfully"}
