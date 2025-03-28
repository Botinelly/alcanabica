from sqlalchemy.orm import Session
from src.models.product import Product as ProductModel
from src.schemas.product import ProductCreate

def create_product(db: Session, product: ProductCreate):
    db_product = ProductModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(ProductModel).all()

def get_product(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

def update_product(db: Session, product_id: int, product_data: ProductCreate):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        return None
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.quantity = product_data.quantity
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()