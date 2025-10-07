from fastapi import APIRouter, Depends, status
from .schemas import UserCreate,  SignupResponse, UserLogin, AdminloginResponse, UserLoginResponse
from .services import UserAuthServices, AdminAuthServices
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session


auth_router = APIRouter()
userAuthService = UserAuthServices()
adminAuthService = AdminAuthServices()

@auth_router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def user_signup(user: UserCreate, session: AsyncSession= Depends(get_session)):
        
        new_user = await userAuthService.user_signup(user, session)
        return new_user

@auth_router.post("/login",response_model=UserLoginResponse, status_code=status.HTTP_202_ACCEPTED)
async def user_login(user: UserLogin, session: AsyncSession= Depends(get_session)):
        user_login = await userAuthService.user_login(user, session=session)

        return user_login

@auth_router.post("/access_token_user", status_code=status.HTTP_201_CREATED)
async def create_new_user_access_token(token:str, session: AsyncSession= Depends(get_session)):
        access_token = await userAuthService.create_new_user_access_token(token, session=session)

        return access_token

@auth_router.post("/admin_signup_check", status_code=status.HTTP_200_OK)
async def admin_signup_check(email:str, session: AsyncSession = Depends(get_session)):
        admin_valid = await adminAuthService.admin_signup_check(email, session)

        return admin_valid

@auth_router.post("/admin_signup")
async def activate_admin(email: str, password, session:AsyncSession=Depends(get_session)):
        admin_activated = await adminAuthService.activate_admin(email, password, session)

        return admin_activated

@auth_router.post("/admin_login",response_model=AdminloginResponse, status_code=status.HTTP_202_ACCEPTED)
async def admin_login(email, password, session: AsyncSession= Depends(get_session)):
        admin_login = await adminAuthService.admin_login(email,password, session=session)

        return admin_login


@auth_router.post("/access_token_admin", status_code=status.HTTP_201_CREATED)
async def create_new_admin_access_token(token:str, session: AsyncSession= Depends(get_session)):
        access_token = await adminAuthService.create_new_admin_access_token(token, session=session)

        return access_token

from src.auth.utils import decode_user_token
@auth_router.post("/test_token")
async def test_token(token: str):
    try:
        # Print token info
        print(f"Token length: {len(token)}")
        print(f"Token starts with: {token[:10]}")
        print(f"Token ends with: {token[-10:]}")
        
        # Try to decode
        payload = decode_user_token(token.strip())
        return {"status": "success", "payload": payload}
    except Exception as e:
        return {"status": "error", "message": str(e)}