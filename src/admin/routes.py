from fastapi import APIRouter, Depends, status
from .services import AdminMainServices
from .schemas import AdminAdd
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.dependencies import get_super_admin
from src.auth.models import Admin
from src.admin.schemas import AdminResponse, AdminDelete

admin_router = APIRouter()
adminMainService = AdminMainServices()


@admin_router.post("/add_staff",response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
async def add_admin(new_admin: AdminAdd, session: AsyncSession = Depends(get_session), SuperAdmin: Admin = Depends(get_super_admin)):
    new_admin = await adminMainService.add_admin(new_admin, session)
    return new_admin

@admin_router.delete("/delete_staff", status_code=status.HTTP_200_OK)
async def delete_admin(admin: AdminDelete, session: AsyncSession = Depends(get_session), SuperAdmin: Admin = Depends(get_super_admin)):
    delete_admin = await adminMainService.delete_admin(admin, session)
    return delete_admin
