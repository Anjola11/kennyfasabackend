from fastapi import APIRouter, Depends, status
from .schemas import UserCreate,  SignupResponse, UserLogin, LoginResponse
from .services import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session


auth_router = APIRouter()
service = UserService()

@auth_router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def user_signup(user: UserCreate, session: AsyncSession= Depends(get_session)):
        
        new_user = await service.user_signup(user, session)
        return new_user

@auth_router.post("/login",response_model=LoginResponse, status_code=status.HTTP_202_ACCEPTED)
async def user_login(user: UserLogin, session: AsyncSession= Depends(get_session)):
        user_login = await service.user_login(user, session=session)

        return user_login