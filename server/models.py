from typing import List, Optional
from uuid import uuid1

from pydantic import BaseModel, Field
from datetime import datetime


class ProductEAN(BaseModel):
    sernum: str = Field(...)
    product_id_type: int = Field(...)
    raw_product_code: str = Field(...)


class Item(BaseModel):
    total: float = Field(...)
    name: str = Field(...)
    price: float = Field(...)
    quantity: float = Field(...)
    product_type: int = Field(...)
    ean: Optional[ProductEAN] = None


class Voucher(BaseModel):
    id: int = Field(default_factory=lambda: uuid1().hex, alias="_id")
    raw_code: str = Field(...)
    code: int = Field(...)
    user: str = Field()
    operation_dttm: datetime = Field(...)
    total_sum: float = Field(..., gt=0)
    retail_place: str = Field()
    address: Optional[str] = None
    items: List[Item] = Field(...)


def response_success(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def response_error(error, code, message):
    return {"error": error, "code": code, "message": message}
