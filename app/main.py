from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from .database import database, engine, metadata
from .schemas import User, UserCreate
from .crud import create_user, get_user, list_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to the database and ensure tables exist at startup
    await database.connect()
    metadata.create_all(engine)
    try:
        yield
    finally:
        await database.disconnect()


app = FastAPI(title="superdev API", lifespan=lifespan)


@app.post("/users/", response_model=User)
async def post_user(user: UserCreate):
    created = await create_user(user)
    return created


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/", response_model=list[User])
async def read_users():
    return await list_users()
