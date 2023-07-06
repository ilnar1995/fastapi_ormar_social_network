from fastapi import APIRouter



from src.user.auth import auth_backend, fastapi_users, SECRET

user_router = APIRouter()


user_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
user_router.include_router(
    fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
)
# user_router.include_router(
#     fastapi_users.get_reset_password_router(
#         SECRET, after_forgot_password=on_after_forgot_password
#     ),
#     prefix="/auth",
#     tags=["auth"],
# )
user_router.include_router(
    fastapi_users.get_verify_router(
    ),
    prefix="/auth",
    tags=["auth"],
)
user_router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])




