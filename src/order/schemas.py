from pydantic import BaseModel
from datetime import datetime
import uuid
from datetime import datetime
from typing import Optional


class OrderCreate(BaseModel):
    customer_id: uuid.UUID
    description: str
    price: float
    quantity: int

class OrderCreatedResponse(BaseModel):
    order_id: uuid.UUID
    customer_id: uuid.UUID
    description: str
    price: float
    quantity: int
    subtotal: float
    status: str
    received_date: datetime
    fulfilled_date: datetime | None
