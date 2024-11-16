# This project doesnt work We are in progress
I am creating my own catalogue of stamps which will be able to show approximate prices from various auctions.
It's not a business project or a plan I'm just combining two hobbies together.

# Basic
Homemade project for creating web app for collecting data about stamps

## How to run
''' python -m uvicorn backend.app.main:app --reload '''

## How to mock database:
Run uvicorn for creating db:
''' python -m uvicorn backend.app.main:app --reload '''

Run this script for powershell windows:
'''
$env:PYTHONPATH="<path to your folder>\stampcollector"
python shared/utils/mock_database/mock_database.py
'''

Now u have data in database!
