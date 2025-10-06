from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User, Admin
from .schemas import UserCreate
from sqlmodel import select
from typing import Optional
from .utils import generate_password_hash, create_access_token, create_refresh_token, decode_token, verify_password_hash
from fastapi import HTTPException, status
from datetime import timedelta, datetime
import jwt
from sqlalchemy.exc import IntegrityError, DatabaseError

access_token_expiry = timedelta(hours=1) 
refresh_token_expiry = timedelta(days=7)

class GeneralServices:
    """Generic method to get Admin/user by email"""
    async def get_by_email(self, model, email: str, session: AsyncSession) -> Optional[object]:
        statement = select(model).where(model.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user
    
    async def get_by_id(self, id: str, session: AsyncSession):
        statement = select(User).where(User.uid == id)
        result = await session.exec(statement)
        user = result.first()
        return user
    


class UserAuthServices(GeneralServices):
    async def user_exists(self, email, session: AsyncSession) -> bool:
        """Check if a user exists"""
        user = await self.get_by_email(User, email, session)
        return user
   
    async def user_signup(self, user: UserCreate, session: AsyncSession):
        """User signup"""

        normalized_email = user.email.lower().strip()

        user_exists = await self.user_exists(normalized_email, session)
        
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        password_hash = generate_password_hash(user.password)
        new_user = User(
            name=user.name.strip().title(),
            email=normalized_email,
            password_hash=password_hash
        )

        session.add(new_user)
        
        try:
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user: Email may already be in use"
            )
        
        except DatabaseError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error: Failed to create user"
            )

        

        
    async def user_login(self, user:UserCreate, session:AsyncSession):
        normalized_email = user.email.lower().strip()
        db_user = await self.get_by_email(User,normalized_email, session=session)

        
        if db_user:
            password_valid = verify_password_hash(user.password, db_user.password_hash)
            if password_valid:
                access_token = create_access_token(
                user_data={
                    'id': str(db_user.uid),
                    "name":db_user.name,
                    "email":db_user.email
                },
                expiry= access_token_expiry
                )
                refresh_token = create_refresh_token(str(db_user.uid), expiry= refresh_token_expiry)

                return {'user': db_user, 'access_token': access_token, 'refresh_token':refresh_token, 'token_type': 'bearer'}

            else: 
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid Email or password'
                )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Email or password'
        )

    async def create_new_access_token(self,token:str, session= AsyncSession):
        try:
            payload = decode_token(token)

            """Verify if the token s a refresh token"""
            token_type = payload.get('type')
            if token_type != 'refresh':
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid Token type. Expected refresh token.'
                )
            
          
        
            """Verify the data"""
            user_id = payload.get('sub')

            user = await self.get_by_id(user_id, session)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            user_data={
                'id': str(user.uid),
                "name":user.name,
                "email":user.email
            }
            new_access_token = create_access_token(user_data, expiry=access_token_expiry)

            return {"access_token":new_access_token, "token_type": "bearer"}
        
        except jwt.ExpiredSignatureError:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token has expired. Please login again.'
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid refresh token'
            )



class AdminAuthServices(GeneralServices):
    async def admin_exists(self, email, session: AsyncSession) -> bool:
        """Check if an admin exists"""
        normalized_email = email.lower().strip()

        admin = await self.get_by_email(Admin, normalized_email, session)
        return admin
    
    async def admin_signup_check(self, email:str, session: AsyncSession):
        normalized_email = email.lower().strip()
        admin = await self.admin_exists(normalized_email, session)

        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email not found. Contact administrator to get added."
            )
        
        if admin.password_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account already activated. Please login instead."
            )
        
        return {"message": "Email verified. Please set your password."}
        
        
    async def admin_signup(self, email:str, password:str, session: AsyncSession):
        normalized_email = email.lower().strip()
        admin = await self.admin_exists(normalized_email, session)

        if not admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Email not found"
            )
        
        if admin.password_hash:  
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password already set. Please login instead."
            )
        
        password_hash = generate_password_hash(password)
        admin.password_hash = password_hash


        try:
            await session.commit()
            await session.refresh(admin)
            return {"message": "Password created successfully"}  
        except DatabaseError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password"
            )
            

        

        


