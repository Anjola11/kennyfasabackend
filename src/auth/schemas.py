from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import Literal

class CustomerCreate(BaseModel):
    name: str
    email: str
    password: str

class CustomerLogin(BaseModel):
    email: str
    password: str

class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

class AdminLogin(BaseModel):
    email: str
    password: str
    
class SignupResponse(BaseModel):
    uid: uuid.UUID
    name: str
    email: str

class CustomerLoginResponse(BaseModel):
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