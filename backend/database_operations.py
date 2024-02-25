from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from backend.schemas import StampResponse, StampTypeResponse
from backend.models import Stamp


# Upravený endpoint
def get_stamp_types(db: Session, stamp_id: int):
    query = text("""
        SELECT stamp.*, stamp_type.*
        FROM stamp
        JOIN stamp_type ON stamp.id = stamp_type.stamp_id
        WHERE stamp.id = :stamp_id
    """)

    result = db.execute(query, {"stamp_id": stamp_id}).fetchall()
    for row in result:
        print(row)
        print("Hodnota plate_flaw:", row[8])

    # Získání dat do listu objektů
    stamp_types = [
        {
            "id": int(row[0]),
            "catalog_number": int(row[1]),
            "emission_id": int(row[2]),
            "name": str(row[3]),
            "country": str(row[4]),
            "photo_path_basic": str(row[5]),
            "stamp_type_id": int(row[6]),
            "stamp_id": int(row[7]),
            "photo_path_type": str(row[8]),
            "description": str(row[9]),
            "type": str(row[10]),
            "color": str(row[11]),
            "quality": str(row[12]),
            "perforation": str(row[13]),
            "plate_flaw": int(row[14]),
            "catalog_price": int(row[15]),
        } for row in result
    ]

    return stamp_types
    