from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class AdminAdd(BaseModel):
    name: str
    email: str
    role: Literal["owner","staff"] = "staff"

class AdminDelete(BaseModel):
    name: str
    email: str
class AdminResponse(BaseModel):
    name: str
    email: str
    role: str
    created_at: datetime