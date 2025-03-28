from fastapi import FastAPI
from src.routes.user import router as router_user
from src.routes.product import router as router_product
import uvicorn
import os

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

app = FastAPI()
app.include_router(router_user)
app.include_router(router_product)

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)