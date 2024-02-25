# This project doesnt work We are in progress

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
