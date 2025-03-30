from typing import Dict, List
from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.models.user import User as UserModel
from src.models.product import Product as ProductModel
from src.database.connection import SessionLocal
import requests
import os

router = APIRouter(prefix="/order", tags=["Mercado Pago"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create-order")
async def create_mercado_pago_order(email: str, raw_products: List[Dict], db: Session = Depends(get_db)):
    # body = await req.json()
    # raw_products = body.get("products", [])  # Ex: [ { "name": "Produto X", "quantity": 2 }, ... ]
    # email = body.get("email")

    if not raw_products or not email:
        raise HTTPException(status_code=400, detail="Produtos e email são obrigatórios")

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    product_names = [p["name"] for p in raw_products]
    db_products = db.query(ProductModel).filter(ProductModel.name.in_(product_names)).all()
    db_product_dict = {p.name: p for p in db_products}

    items = []
    for p in raw_products:
        product = db_product_dict.get(p["name"])
        if not product:
            continue
        quantity = p.get("quantity", 1)
        items.append({
            "title": product.name,
            "quantity": quantity,
            "unit_price": float(product.price)
        })

    payload = {
        "items": items,
        "payer": {"email": email},
        "back_urls": {
            "success": "https://alcanabica.org/success",
            "failure": "https://alcanabica.org/failure",
            "pending": "https://alcanabica.org/pending"
        },
        "auto_return": "approved"
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('MERCADO_PAGO_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.mercadopago.com/checkout/preferences", json=payload, headers=headers)

    if response.ok:
        return {"payment_link": response.json().get("init_point")}

    raise HTTPException(status_code=500, detail="Erro ao gerar pedido")

