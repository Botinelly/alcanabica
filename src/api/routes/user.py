from fastapi import APIRouter, HTTPException, status
from src.models.user import UserCreate, UserUpdate
from src.schemas.user import UserDB
from src.db.db import connect
from typing import List

router = APIRouter()

@router.on_event("startup")
async def startup():
    router.db = await connect()
    await router.db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            cpf TEXT NOT NULL,
            prescription_date DATE NOT NULL,
            association_date DATE NOT NULL,
            products TEXT[]
        )
    """)

@router.on_event("shutdown")
async def shutdown():
    await router.db.close()

@router.post("/users", response_model=UserDB)
async def create_user(user: UserCreate):
    query = """
        INSERT INTO users (name, email, cpf, prescription_date, association_date, products)
        VALUES ($1, $2, $3, $4, $5, $6) RETURNING id
    """
    user_id = await router.db.fetchval(query, user.name, user.email, user.cpf, user.prescription_date, user.association_date, user.products)
    return {"id": user_id, **user.dict()}

@router.get("/users", response_model=List[UserDB])
async def list_users():
    rows = await router.db.fetch("SELECT * FROM users")
    return [dict(row) for row in rows]

@router.get("/users/{user_id}", response_model=UserDB)
async def get_user(user_id: int):
    row = await router.db.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row)

@router.put("/users/{user_id}", response_model=UserDB)
async def update_user(user_id: int, user: UserUpdate):
    existing = await router.db.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    updated = user.dict(exclude_unset=True)
    for key, value in updated.items():
        await router.db.execute(f"UPDATE users SET {key} = $1 WHERE id = $2", value, user_id)
    row = await router.db.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    return dict(row)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    await router.db.execute("DELETE FROM users WHERE id = $1", user_id)
    return {"message": "User deleted"}
