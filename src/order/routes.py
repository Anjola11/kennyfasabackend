from fastapi import APIRouter, Depends, status
from src.order.schemas import OrderCreate, OrderCreatedResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.order.services import OrderServices

order_router = APIRouter()
order_services = OrderServices()

@order_router.post("/signup", response_model=OrderCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order:OrderCreate, session: AsyncSession = Depends(get_session)):
    new_order = await order_services.create_order(order, session)
    return new_order