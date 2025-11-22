from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    # Pydantic v2 config: prefer `from_attributes` instead of deprecated `orm_mode`
    model_config = ConfigDict(from_attributes=True)
