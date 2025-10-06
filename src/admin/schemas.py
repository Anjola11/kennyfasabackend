from pydantic import BaseModel
from typing import Literal

class AdminAdd(BaseModel):
    name: str
    email: str
    role: Literal["owner","staff"] = "staff"
