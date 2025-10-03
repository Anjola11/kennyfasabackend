from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User, Admin
from .schemas import UserCreate
from sqlmodel import select
from typing import Optional
from .utils import generate_password_hash, create_access_token, verify_password_hash
from fastapi import HTTPException, status
from datetime import timedelta


expiry = timedelta(hours=1) 

class GeneralService:
    """Generic method to get Admin/user by email"""
    async def get_by_email(self, model, email: str, session: AsyncSession) -> Optional[object]:
        statement = select(model).where(model.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user


class UserService(GeneralService):
    async def user_exists(self, email, session: AsyncSession) -> bool:
        """Check if a user exists"""
        user = await self.get_by_email(User, email, session)
        return user
   
    async def user_signup(self, user: UserCreate, session: AsyncSession):
        """User signup"""
        user_exists = await self.user_exists(user.email, session)
        
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        password_hash = generate_password_hash(user.password)
        new_user = User(
            name=user.name,
            email=user.email,
            password_hash=password_hash
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

        
    async def user_login(self, user:UserCreate, session:AsyncSession):
        db_user = await self.get_by_email(User,user.email, session=session)

        
        if db_user:
            password_valid = verify_password_hash(user.password, db_user.password_hash)
            if password_valid:
                access_token = create_access_token(
                user_data={
                    'id': str(db_user.uid),
                    "name":db_user.name,
                    "email":db_user.email
                },
                expiry=expiry
            )

            return {
                'user': db_user,
                'access_token': access_token,
                'token_type': 'bearer'
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid Email or password'
            )


   

class AdminService(GeneralService):
    async def admin_exists(self, email, session: AsyncSession) -> bool:
        """Check if an admin exists"""
        admin = await self.get_by_email(Admin, email, session)
        return admin is not None