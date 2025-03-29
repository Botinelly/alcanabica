from pydantic import BaseModel
from typing import List, Dict
from datetime import date
from src.schemas.product import ProductUser

class UserBase(BaseModel):
    name: str
    email: str
    cpf: str
    prescription_date: date
    association_date: date

class ProductRelation(BaseModel):
    product_id: int
    max_amount: int

class UserCreate(UserBase):
    products: List[ProductRelation] # Exemplo: [{"product_id": 1, "limit": 5}]

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    products: List[ProductUser]

    class Config:
        orm_mode = True
