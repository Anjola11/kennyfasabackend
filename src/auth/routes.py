from fastapi import APIRouter, Depends, status
from .schemas import UserCreate, UserResponse
from .services import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session


auth_router = APIRouter()
service = UserService()

@auth_router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def user_signup(user: UserCreate, session: AsyncSession= Depends(get_session)):
        
        new_user = await service.user_signup(user, session)
        return new_user