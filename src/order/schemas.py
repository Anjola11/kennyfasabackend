from pydantic import BaseModel
from datetime import datetime
import uuid


class OrderCreate(BaseModel):
    customer_id: uuid.UUID
    description: str
    price: float
    quantity: int
