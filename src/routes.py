from fastapi import APIRouter
from src.user.routers import user_router
from src.post.router import post_router


routes = APIRouter()

routes.include_router(user_router)

routes.include_router(
    post_router,
    prefix="/post",
    tags=["post"],
)



