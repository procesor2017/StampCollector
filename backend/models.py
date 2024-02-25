from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Emission(Base):
    __tablename__ = 'emission'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    country = Column(String(50), nullable=False)

class Stamp(Base):
    __tablename__ = 'stamp'

    id = Column(Integer, primary_key=True)
    catalog_number = Column(Integer, unique=True, nullable=False)
    emission_id = Column(Integer, ForeignKey('emission.id'), nullable=False)
    name = Column(String(255), nullable=False)
    country = Column(String(50), nullable=False)
    photo_path_basic = Column(String(255), nullable=True)


class StampType(Base):
    __tablename__ = 'stamp_type'

    id = Column(Integer, primary_key=True)
    stamp_id = Column(Integer, ForeignKey('stamp.id'), nullable=False)
    photo_path_type = Column(String(255), nullable=True)
    description = Column(String, nullable=True)
    type = Column(String(50), nullable=False)
    color = Column(String(50), nullable=True)
    quality = Column(String(10), nullable=False)
    perforation = Column(String(50), nullable=True)
    plate_flaw = Column(Integer, nullable=True)
    catalog_price = Column(Float, nullable=False)

class StampSeal(Base):
    __tablename__ = 'stamp_seal'

    id = Column(Integer, primary_key=True)
    stamp_type_id = Column(Integer, ForeignKey('stamp_type.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    photo = Column(String(255), nullable=True)

class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    stamp_type_id = Column(Integer, ForeignKey('stamp_type.id'), nullable=False)
    price = Column(Float, nullable=False)
    sale_date = Column(String, nullable=False)
