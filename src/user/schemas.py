from fastapi_users import models
from pydantic import EmailStr


class User(models.BaseUser):
    pass
    # username: str


class UserCreate(models.CreateUpdateDictModel):
    # username: str
    email: EmailStr
    password: str


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass