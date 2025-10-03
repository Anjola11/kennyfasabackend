from pydantic import BaseModel
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class SignupResponse(BaseModel):
    uid: uuid.UUID
    name: str
    email: str

class LoginResponse(BaseModel):
    user: SignupResponse
    access_token:  str
    token_type: str
