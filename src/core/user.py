from sqlalchemy.orm import Session
from src.models.user import User as UserModel
from src.models.product import Product as ProductModel
from src.schemas.user import UserCreate
from src.schemas.product import ProductCreate
import json

def extract_product_ids(products_field: list[dict]) -> list[int]:
    return [p["product_id"] for p in products_field or []]

def create_user(db: Session, user_data: UserCreate):
    user = UserModel(
        name=user_data.name,
        email=user_data.email,
        cpf=user_data.cpf,
        prescription_date=user_data.prescription_date,
        association_date=user_data.association_date,
        products=[product.__dict__ for product in user_data.products]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    users = db.query(UserModel).all()
    return users

def get_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return user

def create_product_for_user(db: Session, user_id: int, product: ProductCreate):
    db_product = ProductModel(**product.dict(), user_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_user(db: Session, user_id: int, user_data: UserCreate):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()

def get_user_by_cpf(db: Session, cpf: str):
    return db.query(UserModel).filter(UserModel.cpf == cpf).first()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()
