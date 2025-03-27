from fastapi import FastAPI
from src.api.routes.user import router

app = FastAPI()
app.include_router(router)
