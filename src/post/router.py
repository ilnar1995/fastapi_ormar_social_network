from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from src.user.auth import current_active_user
from . import schemas
from . import models
from src.redis import redis_session
from src.post import services

post_router = APIRouter()


@post_router.post('/', status_code=201, response_model=schemas.PostList)
async def add_post(
        schema: schemas.PostCreate, user: models.User = Depends(current_active_user)
):
    current_user = await models.User.objects.get(id=user.id)
    return await models.Post.objects.create(title=schema.title, description=schema.description, user=current_user)


@post_router.get('/', response_model=List[schemas.PostList])
async def get_posts(redis=Depends(redis_session)):
    posts = await models.Post.objects.all()
    for post in posts:
        like, dislike = await services.get_or_set(post, redis)
        post.like_count = like
        post.dislike_count = dislike
    return posts


@post_router.get('/{post_id}', response_model=schemas.PostList)
async def get_post(post_id: int, redis=Depends(redis_session)):
    post = await models.Post.objects.select_related("like_user").get_or_none(id=post_id)
    like, dislike = await services.get_or_set(post, redis)
    post.like_count = like
    post.dislike_count = dislike
    return post


@post_router.post('/{post_id}/add_like', status_code=201)
async def add_like(
        post_id: int, user: models.User = Depends(current_active_user), redis=Depends(redis_session)
):
    return await services.add_like_or_dislike(post_id, user, redis, False)


@post_router.post('/{post_id}/add_dislike', status_code=201)
async def add_dislike(
        post_id: int, user: models.User = Depends(current_active_user), redis=Depends(redis_session)
):
    return await services.add_like_or_dislike(post_id, user, redis, True)
