from pydantic import BaseModel, validator
from datetime import datetime



class PostCreate(BaseModel):
    title: str
    description: str = 'default description'


class PostList(PostCreate):
    id: int
    create_at: datetime
    user: str
    like_count: int = 0
    dislike_count: int = 0

    @validator("user", pre=True)
    def toppings_validate(cls, date):
        return str(date.get('id'))
