from sqlmodel.ext.asyncio.session import  AsyncSession
from .models import User, Admin
from sqlmodel import select
from typing import Optional

class UserService:
    """Generic method to get Admin/user by email"""
    async def get_by_email(self, model, email:str, session: AsyncSession) -> Optional[object]:
        statement = select(model).where(model.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user

    async def user_exists(self, email, session: AsyncSession) -> bool:
        """Check if a user exists"""
        user = await self.get_by_email(User, email, session)

        return user is not None
    
    async def admin_exists(self, email, session: AsyncSession) -> bool:
        """Check if an admin exists"""
        admin = await self.get_by_email(Admin, email, session)

        return admin is not None
    