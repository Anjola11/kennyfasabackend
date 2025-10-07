from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import Literal

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
    role: Literal["owner","staff"] = "staff"

class AdminLogin(BaseModel):
    email: str
    password: str
    
class SignupResponse(BaseModel):
    uid: uuid.UUID
    name: str
    email: str

class UserLoginResponse(BaseModel):
    uid: uuid.UUID
    name: str
    email: str
    access_token:  str
    refresh_token: str
    token_type: str
    
class AdminloginResponse(BaseModel):
    uid: uuid.UUID
    name: str
    email: str
    access_token:  str
    refresh_token: str
    token_type: str