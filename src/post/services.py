from src.post import models
from src.config import TIME_CACHE


async def get_or_set(post, redis):
    list_like_dislike = []
    like, dislike = await redis.hmget(f"post_{post.id}_cache", 'like', 'dislike')
    if like is not None and dislike is not None:
        list_like_dislike = [like, dislike]
    if list_like_dislike == []:
        like = await post.like_user.filter(likeordislike__dislike=False).count()
        dislike = await post.like_user.filter(likeordislike__dislike=True).count()
        # заносим в редис
        values = {
            'like': like,
            'dislike': dislike
        }
        await redis.hset(f"post_{post.id}_cache", mapping=values)
        await redis.expire(f"post_{post.id}_cache", TIME_CACHE)
    else:
        print('-------------------from cache---------------------')
        like = list_like_dislike[0]
        dislike = list_like_dislike[1]
    # await redis.flushdb()
    return like, dislike


async def update_cache(post, redis, like_change: int, dislike_change: int):
    like, dislike = await redis.hmget(f"post_{post.id}_cache", 'like', 'dislike')
    if like is not None and dislike is not None:
        values = {
            'like': int(like) + like_change,
            'dislike': int(dislike) + dislike_change
        }
        await redis.hset(f"post_{post.id}_cache", mapping=values)
        await redis.expire(f"post_{post.id}_cache", TIME_CACHE)


async def add_like_or_dislike(post_id, user, redis, dislike: bool):
    _post = await models.Post.objects.select_related("like_user").filter(id=post_id).exists()
    if not _post:
        return {'status': 'post not exist'}
    post = await models.Post.objects.select_related("like_user").filter(like_user__id=user.id, id=post_id).get_or_none()
    if not post:
        post = await models.Post.objects.select_related("like_user").get(id=post_id)
        if post.user.id == user.id:
            return {'status': "you can't rate own post"}
        current_user = await models.User.objects.get(id=user.id)
        await post.like_user.add(current_user, dislike=dislike)
        if dislike:
            await update_cache(post, redis, 0, 1)
        else:
            await update_cache(post, redis, 1, 0)
        return {'status': 'success'}
    else:
        if post.like_user[0].likeordislike.dislike != dislike:
            if dislike:
                await update_cache(post, redis, -1, 1)
            else:
                await update_cache(post, redis, 1, -1)
            # await post.like_user[0].likeordislike.load()
            # await post.like_user[0].likeordislike.update(dislike=dislike)
            await post.like_user.filter(id=user.id).update(likeordislike={"dislike": dislike})
            return {'status': 'success'}
        else:
            return {'status': 'already in list if like'}
