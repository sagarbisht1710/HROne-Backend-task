from pydantic import BaseModel, Field
from typing import List

class OrderItemCreate(BaseModel):
    productId: str = Field(..., min_length=1)
    qty: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    userId: str = Field(..., min_length=1)
    items: List[OrderItemCreate]