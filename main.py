from fastapi import FastAPI, Depends, HTTPException, Security
from src.routes.user import router as router_user
from src.routes.product import router as router_product
from src.routes.order import router as router_order
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from src.database.connection import SessionLocal
from src.core.verification import clean_expired_codes
import uvicorn
import asyncio
import os

from dotenv import load_dotenv

load_dotenv()



HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
API_KEY_NAME = os.getenv("API_KEY_NAME")
API_KEY = os.getenv("API_KEY")

app = FastAPI()

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Invalid or missing API Key"
    )

app.include_router(router_user, dependencies=[Depends(get_api_key)])
app.include_router(router_product, dependencies=[Depends(get_api_key)])
app.include_router(router_order)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://34.77.31.159",
        "http://23.251.142.192",
        "https://34.77.31.159",
        "https://23.251.142.192",
        "https://185.230.63.107",
        "http://185.230.63.107",
        "http://loja.alcanabica.org",
        "https://loja.alcanabica.org",
        "https://alcanabica-a5sf.onrender.com",
        "http://alcanabica-a5sf.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_background_tasks():
    async def cleaner_loop():
        while True:
            await asyncio.sleep(600)
            try:
                db = SessionLocal()
                clean_expired_codes(db)
            finally:
                db.close()
    asyncio.create_task(cleaner_loop())


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)