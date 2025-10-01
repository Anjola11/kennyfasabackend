from fastapi import APIRouter
from .schemas import UserCreate
auth_router = APIRouter()

@auth_router.post("/signup")
def signup(user: UserCreate):
    return user.name