from src.core import verification as vcore
from src.schemas.verification import CodeVerify
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.user import User, UserCreate
from src.core import user as crud
from src.database.connection import SessionLocal
from src.models.product import Product as ProductModel

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def extract_product_ids(products_field: list[dict]) -> list[int]:
    return [p["product_id"] for p in products_field or []] 

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    products = db.query(ProductModel).filter(ProductModel.id.in_(extract_product_ids(db_user.products))).all()
    return {
        **db_user.__dict__,
        "products": products
    }

@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    result = []
    for user in users:
        product_ids = [p["product_id"] for p in user.products or []]
        product_limits = {p["product_id"]: p["max_amount"] for p in user.products or []}
        products = db.query(ProductModel).filter(ProductModel.id.in_(product_ids)).all()
        product_response = []
        for product in products:
            product_response.append({
                "product_id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "quantity": product.quantity,
                "max_amount": product_limits.get(product.id, 0)
            })
        result.append({
            **user.__dict__,
            "products": product_response
        })
    return result

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    product_ids = [p["product_id"] for p in user.products or []]
    product_limits = {p["product_id"]: p["max_amount"] for p in user.products or []}

    products = db.query(ProductModel).filter(ProductModel.id.in_(product_ids)).all()

    product_response = []
    for product in products:
        product_response.append({
            "product_id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "max_amount": product_limits.get(product.id, 0)
        })

    return {
        **user.__dict__,
        "products": product_response
    }

@router.put("/{user_id}")
def update_user(user_id: int, data: UserCreate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)

@router.get("/cpf/{cpf}", response_model=User)
def read_user_by_cpf(cpf: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_cpf(db, cpf)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        **user.__dict__,
        "products": db.query(ProductModel)
            .filter(ProductModel.id.in_(extract_product_ids(user.products) or []))
            .all()
    }

@router.get("/email/{email}")
def get_user(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    product_ids = [p["product_id"] for p in user.products or []]
    product_limits = {p["product_id"]: p["max_amount"] for p in user.products or []}

    products = db.query(ProductModel).filter(ProductModel.id.in_(product_ids)).all()

    product_response = []
    for product in products:
        product_response.append({
            "product_id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "max_amount": product_limits.get(product.id, 0)
        })

    return {
        **user.__dict__,
        "products": product_response,
        "products_string":  [f"{x.name} | R${x.price},00/g" for x in products]

    }

@router.get("/email/{email}/send-code")
def send_verification_code(email: str, db: Session = Depends(get_db)):
    message = "Código enviado com sucesso para o e-mail."
    if vcore.create_and_send_code(db, email) == 000000:
        message = "Esse e-mail não está cadastrado." 
    return {"message": message}

@router.post("/validate")
def validate_code(payload: CodeVerify, db: Session = Depends(get_db)):
    if vcore.validate_code(db, payload.email, payload.code):
        return {"valid": True, "message": "Código válido"}
    return {"valid": False, "message": "Código inválido ou expirado"}
