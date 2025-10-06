from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, timezone
from typing import Optional, Literal
from pydantic import field_validator

def utc_now():
    return datetime.now(timezone.utc)

class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4, 
        primary_key=True, 
        index=True
    )
    name: str 
    email: str = Field(unique=True, index=True)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(pg.TIMESTAMP(timezone=True))
        )



class Admin(SQLModel, table=True):
    __tablename__ = "admins"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4, 
        primary_key=True, 
        index=True, 
        unique=True
    )
    name: str 
    email: str = Field(unique=True, index=True)
    password_hash: Optional[str] = Field(None)
    role: str
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(pg.TIMESTAMP(timezone=True))
        )


    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        if value not in ["owner","staff"]:
            raise ValueError("Enter either owner or staff as role")
        return value