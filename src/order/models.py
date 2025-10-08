from sqlmodel import SQLModel, Field, Column
import uuid
from datetime import datetime, timezone
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from pydantic import field_validator, model_validator

def utc_now():
    return datetime.now(timezone.utc)


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    customer_id: uuid.UUID
    description: str
    price: float
    quantity: int
    subtotal: float = Field(default=0.0)
    status: str = Field(default='pending')
    received_date: datetime = Field(
        default_factory= utc_now,
        sa_column=Column(pg.TIMESTAMP(timezone=True))
    )
    fulfilled_date: Optional[datetime] = Field(None)

    @field_validator("status")
    @classmethod

    def validate_status(cls, value):
        if value not in ['pending','fulfilled']:
            raise ValueError("Enter either pending or fulfilled")
        return value
    

    @model_validator(mode="before")
    @classmethod
    def calculate_subtotal(cls, values):
        subtotal = float(values['price']) * float(values['quantity'])
        values['subtotal'] = subtotal

        return values
