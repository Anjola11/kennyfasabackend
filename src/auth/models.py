from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, timezone
from typing import Optional

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
    role: str = Field(default="admin")
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(pg.TIMESTAMP(timezone=True))
        )
