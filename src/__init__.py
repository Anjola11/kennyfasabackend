from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router
from src.admin.routes import admin_router
from src.order.routes import order_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("---Server Started---")
    await init_db()

    yield
    print("----Server Closed----")

app = FastAPI(
    title="KennyFasa API",
    description="KennyFasa lab website endpoints",
    lifespan=lifespan
)



@app.get("/", tags=["Testing"])
def testing():
    return "Working"

app.include_router(auth_router, prefix="/api/kennyfasa", tags=["Authentication"])
app.include_router(admin_router, prefix="/api/kennyfasa/admin", tags=["Admin Main Services"])
app.include_router(order_router, prefix="/api/kennyfasa/order", tags=["Order"])