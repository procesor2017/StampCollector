# What need to be done?
Database (SQLite)
Backend (python, fastapi)
Frontend (Combination => Python generate html and bootstrap doing others thing)

# Requirements for using
Adding Information:
    - Reading information from auction house
        - Burda
    - Adding information manualy

Usage:
- user can found any stamps
- User create his own list what he has and what he doenst have
- User can have lot of information about stamps
    - usefull links
    - For translate color etc

Security:
- Without login u shouldnt be able to what user has for stamps

## Database and object model
Stamps is in Emision
Emision is In Land

DB:
StampBase table:
stamp_id => Id in my own database
catalog number
photo_path_base
emmision_id

StampTypeBase  table:
stamp_id (from StampBase)
photo_path_type
description 
type_name (I, III,  IIa etc.)
color
perforation (handcut, 6 1/2 etc.)
plate_flaw (DV or VV)
catalog_price_superb
catalog_price_extra_fine
catalog_price_very_fine
catalog_price_fine
catalog_price_avg
catalog_price_poor
catalog_price_post_cover

Emission table:
emission_id
name
country
issue_year

