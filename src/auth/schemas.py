from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str