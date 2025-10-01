from fastapi import APIRouter, Depends
from .schemas import UserCreate
from .services import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session


auth_router = APIRouter()

@auth_router.post("/signup")
async def user_signup(user: UserCreate, session: AsyncSession= Depends(get_session)):
        service = UserService()
        new_user = await service.user_signup(user, session)
        return new_user