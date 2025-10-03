from pydantic import BaseModel
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    uid: uuid.UUID
    name: str
    email: str
    created_at: datetime