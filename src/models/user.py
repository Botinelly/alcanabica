from sqlalchemy import Column, Integer, String, Date, ARRAY, JSON
from sqlalchemy.orm import relationship
from src.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    cpf = Column(String, unique=True)
    prescription_date = Column(Date)
    association_date = Column(Date)
    products = Column(JSON, nullable=True)

