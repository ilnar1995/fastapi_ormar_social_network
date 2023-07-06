import datetime
import ormar
from typing import Optional, Union, Dict, List
from src.core.db import MainMata

from src.user.models import User


class LikeOrDislike(ormar.Model):
    class Meta(MainMata):
        pass

    id: int = ormar.Integer(primary_key=True)
    dislike: bool = ormar.Boolean(default=False)


class Post(ormar.Model):
    class Meta(MainMata):
        pass

    like_count: int = 0
    dislike_count: int = 0
    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=50)
    description: str = ormar.String(max_length=500)
    create_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    user: Optional[Union[User, Dict]] = ormar.ForeignKey(User, related_name="user_post")

    like_user: Optional[Union[List[User], Dict]] = ormar.ManyToMany(
        User, related_name="like_users", through=LikeOrDislike
    )
