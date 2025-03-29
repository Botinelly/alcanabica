from pydantic import BaseModel


class ProductSummary(BaseModel):
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True

class ProductUser(ProductSummary):
    max_amount: int

class ProductCreate(ProductSummary):
    quantity: int

class Product(ProductCreate):
    id: int
