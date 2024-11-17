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

    emission_id = Column(Integer, ForeignKey('emission.emission_id'), nullable=False)
    emission = relationship('Emission', back_populates='stamps')

    stamp_types = relationship("StampTypeBase", back_populates="stamp")
class StampTypeBase(Base):
    __tablename__ = 'stamp_type_base'
    
    stamp_type_id = Column(Integer, primary_key=True)
    stamp_id = Column(Integer, ForeignKey('stamp_base.stamp_id'), nullable=False)
    photo_path_type = Column(String)
    description = Column(String)
    type_name = Column(String)
    color = Column(String)
    paper = Column(String)
    perforation = Column(String)
    plate_flaw = Column(String)
    catalog_price_superb = Column(Float)
    catalog_price_extra_fine = Column(Float)
    catalog_price_very_fine = Column(Float)
    catalog_price_fine = Column(Float)
    catalog_price_avg = Column(Float)
    catalog_price_poor = Column(Float)
    catalog_price_post_cover = Column(Float)

    # Relace pro hlavní známku
    stamp = relationship("StampBase", back_populates="stamp_types")
    
    # Přidejte metodu pro převod na slovník
    def as_dict(self):
        return {
            "stamp_type_id": self.stamp_type_id,
            "stamp_id": self.stamp_id,
            "photo_path_type": self.photo_path_type,
            "description": self.description,
            "type_name": self.type_name,
            "color": self.color,
            "paper": self.paper,
            "perforation": self.perforation,
            "plate_flaw": self.plate_flaw,
            "catalog_price_superb": self.catalog_price_superb,
            "catalog_price_extra_fine": self.catalog_price_extra_fine,
            "catalog_price_very_fine": self.catalog_price_very_fine,
            "catalog_price_fine": self.catalog_price_fine,
            "catalog_price_avg": self.catalog_price_avg,
            "catalog_price_poor": self.catalog_price_poor,
            "catalog_price_post_cover": self.catalog_price_post_cover
        }