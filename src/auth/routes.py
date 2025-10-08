from fastapi import APIRouter, Depends, status
from .schemas import CustomerCreate,  SignupResponse, CustomerLogin, AdminloginResponse, CustomerLoginResponse
from .services import CustomerAuthServices, AdminAuthServices
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session


auth_router = APIRouter()
customerAuthService = CustomerAuthServices()
adminAuthService = AdminAuthServices()

@auth_router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def customer_signup(customer: CustomerCreate, session: AsyncSession= Depends(get_session)):
        
        new_customer = await customerAuthService.customer_signup(customer, session)
        return new_customer

@auth_router.post("/login",response_model=CustomerLoginResponse, status_code=status.HTTP_202_ACCEPTED)
async def customer_login(customer: CustomerLogin, session: AsyncSession= Depends(get_session)):
        customer_login = await customerAuthService.customer_login(customer, session=session)

        return customer_login

@auth_router.post("/access_token_customer", status_code=status.HTTP_201_CREATED)
async def create_new_customer_access_token(token:str, session: AsyncSession= Depends(get_session)):
        access_token = await customerAuthService.create_new_customer_access_token(token, session=session)

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

from src.auth.utils import decode_customer_token
@auth_router.post("/test_token")
async def test_token(token: str):
    try:
        # Print token info
        print(f"Token length: {len(token)}")
        print(f"Token starts with: {token[:10]}")
        print(f"Token ends with: {token[-10:]}")
        
        # Try to decode
        payload = decode_customer_token(token.strip())
        return {"status": "success", "payload": payload}
    except Exception as e:
        return {"status": "error", "message": str(e)}