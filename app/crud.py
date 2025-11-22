from .database import database
from .models import users
from .schemas import UserCreate


async def create_user(user: UserCreate):
    query = users.insert().values(name=user.name, email=user.email)
    user_id = await database.execute(query)
    # use Pydantic v2 `model_dump()` to avoid deprecated `.dict()` usage
    data = user.model_dump()
    data["id"] = user_id
    return data


async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


async def list_users():
    query = users.select()
    return await database.fetch_all(query)
