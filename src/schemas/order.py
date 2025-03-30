from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class OrderResponse(BaseModel):
    id: int
    user_id: int
    order_code: str
    status: str
    created_at: datetime
    products: List[Dict]

    class Config:
        orm_mode = True
