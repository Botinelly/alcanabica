from pydantic import BaseModel
from typing import List
from datetime import date
from src.schemas.product import ProductSummary

class UserBase(BaseModel):
    name: str
    email: str
    cpf: str
    prescription_date: date
    association_date: date

class UserCreate(UserBase):
    products: List[int] = []

class User(UserBase):
    id: int
    products: List[ProductSummary]

    class Config:
        orm_mode = True
