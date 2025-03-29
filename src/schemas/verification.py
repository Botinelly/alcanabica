from pydantic import BaseModel

class CodeVerify(BaseModel):
    email: str
    code: str
