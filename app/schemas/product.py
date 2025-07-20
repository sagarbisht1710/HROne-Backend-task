from pydantic import BaseModel, Field, field_validator
from typing import List

class SizeEntry(BaseModel):
    size: str = Field(..., min_length=1, max_length=32)
    quantity: int = Field(ge=0)

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., ge=0)
    sizes: List[SizeEntry]

    @field_validator("sizes")
    @classmethod
    def unique_sizes(cls, v):
        labels = [s.size.lower() for s in v]
        if len(labels) != len(set(labels)):
            raise ValueError("Duplicate size labels in sizes array")
        return v