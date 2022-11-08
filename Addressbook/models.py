from sqlalchemy import Column, Integer, String
from .database import Base


class BookAddressess(Base):
    __tablename__ = "bookaddressess"
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String)
    street = Column(String)
    city = Column(String)
    address = Column(String)
    latitude = Column(String)
    longitude = Column(String)