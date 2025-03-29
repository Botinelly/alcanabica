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

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    products = db.query(ProductModel).filter(ProductModel.id.in_(db_user.products)).all()
    return {
        **db_user.__dict__,
        "products": products
    }

@router.get("/", response_model=List[User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return [
        {
            **u.__dict__,
            "products": db.query(ProductModel)
                .filter(ProductModel.id.in_(u.products or []))
                .all()
        }
        for u in users
    ]


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        **user.__dict__,
        "products": db.query(ProductModel)
            .filter(ProductModel.id.in_(user.products or []))
            .all()
    }


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user_data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        **updated.__dict__,
        "products": updated.product_objects
    }

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
            .filter(ProductModel.id.in_(user.products or []))
            .all()
    }

@router.get("/email/{email}", response_model=User)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        **user.__dict__,
        "products": db.query(ProductModel)
            .filter(ProductModel.id.in_(user.products or []))
            .all()
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
