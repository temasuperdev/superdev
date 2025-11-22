from fastapi import FastAPI, HTTPException
from .database import database, engine, metadata
from .schemas import User, UserCreate
from .crud import create_user, get_user, list_users

app = FastAPI(title="superdev API")


@app.on_event("startup")
async def startup():
    await database.connect()
    # create tables if they don't exist
    metadata.create_all(engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


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
