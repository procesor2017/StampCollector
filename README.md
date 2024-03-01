# This project doesnt work We are in progress
I am creating my own catalogue of stamps which will be able to show approximate prices from various auctions.
It's not a business project or a plan I'm just combining two hobbies together.

# Basic
Homemade project for creating web app for collecting data about stamps

# Installation
## Init DB
```
python backend/init_db.py
```
## Add data to DB
```
python backend/mock_data.py
```

## Run BackEnd
```
python -m uvicorn backend.main:app --port 8080 --reload
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## Run FrontEnd
```
 $ cd frontend
 $ npm run serve
```

## What we need to add
- Post Cover
- add additional information for emmision (different paper etc. 1890 emission etc.)
- for stamps
