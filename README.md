# This project doesnt work 
## We are in progress
I am creating my own catalogue of stamps which will be able to show approximate prices from various auctions.
It's not a business project or a plan I'm just combining two hobbies together.

# Basic
Homemade project for creating web app for collecting data about stamps

# Web APp
## How to run
``` python -m uvicorn backend.app.main:app --reload ```

## How to mock database:
Run uvicorn for creating db:
```
 python -m uvicorn backend.app.main:app --reload 
```
Run this script for powershell windows:
```
$env:PYTHONPATH="<path to your folder>\stampcollector"
python shared/utils/mock_database/mock_database.py
```

Now u have data in database!

# Desktop
```
python -m desktop
```

## Swagger
http://127.0.0.1:8000/docs

##  Legal proclamation
This code is intended only for processing publicly available PDF files for personal use.
Before using it, please make sure that your use is in accordance with the terms of the data source.


## Auction which u should definately follow
https://www.cherrystoneauctions.com
https://www.davidfeldman.com
https://heinrich-koehler.de
https://www.stanleygibbons.com/


