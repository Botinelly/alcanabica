from sqlalchemy.orm import Session
from src.models.user import User as UserModel
from src.models.product import Product as ProductModel
from src.schemas.user import UserCreate
from src.schemas.product import ProductCreate

def create_user(db: Session, user_data: UserCreate):
    user = UserModel(
        name=user_data.name,
        email=user_data.email,
        cpf=user_data.cpf,
        prescription_date=user_data.prescription_date,
        association_date=user_data.association_date,
        products=user_data.products
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    users = db.query(UserModel).all()
    for user in users:
        user.product_objects = db.query(ProductModel).filter(ProductModel.id.in_(user.products)).all()
    return users

def get_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        user.product_objects = db.query(ProductModel).filter(ProductModel.id.in_(user.products)).all()
    return user

def create_product_for_user(db: Session, user_id: int, product: ProductCreate):
    db_product = ProductModel(**product.dict(), user_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_user(db: Session, user_id: int, user_data: UserCreate):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return None
    user.name = user_data.name
    user.email = user_data.email
    user.cpf = user_data.cpf
    user.prescription_date = user_data.prescription_date
    user.association_date = user_data.association_date
    user.products = user_data.products
    db.commit()
    db.refresh(user)
    user.product_objects = db.query(ProductModel).filter(ProductModel.id.in_(user.products)).all()
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()