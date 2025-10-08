from src.order.models import Order
from src.order.schemas import OrderCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import DatabaseError
from fastapi import HTTPException, status

class OrderServices:

    async def create_order(self, order:OrderCreate, session:AsyncSession):
        new_order = Order(**order.model_dump()
            )
        
        session.add(new_order)
        try:
            await session.commit()
            await session.refresh(new_order)
            return new_order
        except DatabaseError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create order"
            )
        