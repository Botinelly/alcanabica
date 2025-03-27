from fastapi import FastAPI
from src.api.routes.user import router
import uvicorn
import os

HOST = os.getenv("APP_HOST", "0.0.0.0")
PORT = int(os.getenv("APP_PORT", 8000))

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)