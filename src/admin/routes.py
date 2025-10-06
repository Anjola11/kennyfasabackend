from fastapi import APIRouter, Depends, status
from .services import AdminMainServices
from .schemas import AdminAdd
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

admin_router = APIRouter()
adminMainService = AdminMainServices()

@admin_router.post("/add_staff", status_code=status.HTTP_201_CREATED)
async def add_admin(admin: AdminAdd, session: AsyncSession = Depends(get_session)):
    admin = await adminMainService.add_admin(admin, session)
    return admin

