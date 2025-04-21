from datetime import datetime
from typing import Dict, List
from fastapi import APIRouter, Request, HTTPException, status, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.schemas.order import OrderResponse
from src.models.order import Order
from src.models.user import User as UserModel
from src.models.product import Product as ProductModel
from src.database.connection import SessionLocal
from src.utils.email import send_order_email
import requests
import os
import json
import uuid

router = APIRouter(prefix="/order", tags=["Mercado Pago"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateOrderDTO(BaseModel):
    email: str
    raw_products: List[Dict]

@router.post("/create-order")
async def create_mercado_pago_order(data: CreateOrderDTO, db: Session = Depends(get_db)):
    email = data.email
    raw_products = data.raw_products
    # body = await req.json()
    # raw_products = body.get("products", [])  # Ex: [ { "name": "Produto X", "quantity": 2 }, ... ]
    # email = body.get("email")

    if not raw_products or not email:
        raise HTTPException(status_code=400, detail="Produtos e email são obrigatórios")

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    product_names = [p["title"] for p in raw_products]
    db_products = db.query(ProductModel).filter(ProductModel.name.in_(product_names)).all()
    db_product_dict = {p.name: p for p in db_products}

    items = [
        {
            "product_id": 0,
            "title": "Frete",
            "quantity": 1,
            "unit_price": float(50)
        }
    ]
    for p in raw_products:
        product = db_product_dict.get(p["title"])
        if not product:
            continue
        quantity = p.get("quantity", 0)
        if quantity != 0:
            items.append({
                "product_id": product.id,
                "title": product.name,
                "quantity": quantity,
                "unit_price": float(product.price)
            })

    order_code = str(uuid.uuid4())[:8].upper()

    payload = {
        "items": items,
        "payer": {"email": email},
        "back_urls": {
            "success": "https://alcanabica.org/success",
            "failure": "https://alcanabica.org/failure",
            "pending": "https://alcanabica.org/pending"
        },
        "auto_return": "approved",
        "external_reference": order_code
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('MERCADO_PAGO_ACCESS_TOKEN')}",
        "Content-Type": "application/json",
    }

    response = requests.post("https://api.mercadopago.com/checkout/preferences", json=payload, headers=headers)
    if response.ok:
        pay_link = response.json().get("init_point")
        send_order_email(email, items, pay_link, order_code)
        send_order_email('alcanoreply@gmail.com', items, pay_link, order_code)

        for i in items:
            db_order = Order(
                user_id=user.id,
                order_code=order_code,
                status="pending",
                created_at=datetime.utcnow(),
                products=json.dumps(items)
            )
            db.add(db_order)
            db.commit()
            db.add(db_order)
        db.commit()

        return {"payment_link": pay_link, "order_resume": items,  "order_code": order_code}
    
    raise HTTPException(status_code=500, detail="Erro ao gerar pedido")

@router.post("/webhook")
async def mercado_pago_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    external_reference = payload.get("data", {}).get("external_reference")
    payment_status = payload.get("data", {}).get("status")

    if external_reference and payment_status:
        db.query(Order).filter(Order.order_code == external_reference).update({"status": payment_status})
        db.commit()

    return {"status": "ok"}

@router.get("/{email}", response_model=list[OrderResponse])
def get_orders_by_email(
    email: str,
    status_filter: str = Query(None, alias="status"),
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    query = db.query(Order).filter(Order.user_id == user.id)

    if status_filter:
        query = query.filter(Order.status == status_filter)

    orders = query.all()
    return orders
