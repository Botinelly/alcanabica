from pydantic import BaseModel, EmailStr
from typing import List
from datetime import date

class UserBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    prescription_date: date
    association_date: date
    products: List[str]

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    cpf: str | None = None
    prescription_date: date | None = None
    association_date: date | None = None
    products: List[str] | None = None
