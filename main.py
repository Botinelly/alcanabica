from fastapi import FastAPI, Depends, HTTPException, Security
from src.routes.user import router as router_user
from src.routes.product import router as router_product
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
import uvicorn
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

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)