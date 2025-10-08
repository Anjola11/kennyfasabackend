from src.auth.services import AdminAuthServices
from src.admin.schemas import AdminAdd
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from src.auth.models import Admin
from sqlalchemy.exc import DatabaseError
adminAuthService = AdminAuthServices()

class AdminMainServices():
    async def add_admin(self, admin: AdminAdd, session: AsyncSession):
        admin_exists = await adminAuthService.admin_exists(admin.email, session)
        if admin_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin already exists"
            )
        
        admin = Admin(
            name = admin.name,
            email = admin.email.strip().lower(),
            role = admin.role
        )
        
        session.add(admin)

        try:
            await session.commit()
            return admin
        except DatabaseError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = "Failed to add admin"
            )
        
    async def delete_admin(self, admin, session: AsyncSession):
        admin_exists = await adminAuthService.admin_exists(admin.email, session)

        if not admin_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Admin not found"
            )
    
        try:
            await session.delete(admin_exists)
            await session.commit()
            return {"message": "Admin deleted successfully"}
        except DatabaseError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete admin"
            )


