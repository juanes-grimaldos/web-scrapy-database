from sqlalchemy import Column, Integer, String, Date
from data_bases.model.declarative_base import Base
from sqlalchemy import ForeignKey



class Fridges(Base):
    __tablename__ = 'fridges'

    link = Column(String, primary_key=True)
    product = Column(String)
    price = Column(Integer)
    seller = Column(String)

class Specs(Base):
    __tablename__ = 'specs'

    id = Column(Integer, primary_key=True)
    fridge_link = Column(String, ForeignKey('fridges.link'), unique=True)
    storage = Column(String)
    size = Column(String) # width x height x depth
    energy = Column(String)
    color = Column(String)
    date = Column(Date)