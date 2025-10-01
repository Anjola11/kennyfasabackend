from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import Config


engine = create_async_engine(
    url = Config.DATABASE_URL,
    echo = True
)

async def init_db():
    async with engine.begin() as conn:
        from src.auth.models import user
        from src.auth.models import admins

        await conn.run_sync(SQLModel.metadata.create_all)