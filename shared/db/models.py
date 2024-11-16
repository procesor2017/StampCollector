from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Country(Base):
    __tablename__ = 'country'
    
    country_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    emissions = relationship('Emission', back_populates='country')

class Emission(Base):
    __tablename__ = 'emission'
    
    emission_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    issue_year = Column(Integer, nullable=False)

    country_id = Column(Integer, ForeignKey('country.country_id'))
    country = relationship('Country', back_populates='emissions')
    stamps = relationship('StampBase', back_populates='emission')

class StampBase(Base):
    __tablename__ = 'stamp_base'
    
    stamp_id = Column(Integer, primary_key=True)
    catalog_number = Column(String, nullable=False)
    photo_path_base = Column(String, nullable=False)
    name = Column(String, nullable=False)

    emission_id = Column(Integer, ForeignKey('emission.emission_id'))
    emission = relationship('Emission', back_populates='stamps')

class StampTypeBase(Base):
    __tablename__ = 'stamp_type_base'
    
    stamp_id = Column(Integer, ForeignKey('stamp_base.stamp_id'), primary_key=True)
    photo_path_type = Column(String, nullable=False)
    description = Column(String)
    type_name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    paper = Column(String, nullable=False)
    perforation = Column(String, nullable=False)
    plate_flaw = Column(String, nullable=False)
    catalog_price_superb = Column(Float)
    catalog_price_extra_fine = Column(Float)
    catalog_price_very_fine = Column(Float)
    catalog_price_fine = Column(Float)
    catalog_price_avg = Column(Float)
    catalog_price_poor = Column(Float)
    catalog_price_post_cover = Column(Float)
