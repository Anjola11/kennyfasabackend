from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from src.auth.utils import decode_user_token, decode_admin_token
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.auth.services import GeneralServices
from src.auth.models import Admin, User
import jwt

security = HTTPBearer()
general_services = GeneralServices()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: AsyncSession =Depends(get_session)):

    try:
        token = credentials.credentials.strip()
        payload = decode_user_token(token)

        if payload.get("type") != 'access':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid Token"
            )
        
        user_id = payload.get('sub')

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='invalid token'
            )
        
        user = await general_services.get_by_id(User, user_id, session)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User not found'
            )
        
        
        return user
    
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token expired"
        )
    
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )
    
        

async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security), session: AsyncSession= Depends(get_session)):

    try:
        token = credentials.credentials.strip()

        payload = decode_admin_token(token)

        if payload.get('type') != 'access':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= 'invalid token'
            )
        
        admin_id = payload.get('sub')

        if not admin_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='invalid token'
            )
        
        admin = await general_services.get_by_id(Admin, admin_id, session)

        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User not found'
            )
        
        if not admin.password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='account not activated. set a pasword first'
            )
        
        return admin
    
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token expired"
        )
    
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )
    

async def get_super_admin(admin: Admin= Depends(get_current_admin)):

    if admin.role != 'owner':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not authorized to access this"
        )
    
    return admin