from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router

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



@app.get("/")
def testing():
    return "Working"

app.include_router(auth_router, prefix="/api/kennyfasa")