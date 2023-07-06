import ormar
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase

from src.core.db import MainMata
from src.user.schemas import UserDB

class User(OrmarBaseUserModel):
    class Meta(MainMata):
        tablename = "user"

    id = ormar.UUID(primary_key=True, uuid_format="string")
    email = ormar.String(index=True, unique=True, nullable=False, max_length=255)
    hashed_password = ormar.String(nullable=False, max_length=255)
    is_active = ormar.Boolean(default=True, nullable=False)
    is_superuser = ormar.Boolean(default=False, nullable=False)
    is_verified = ormar.Boolean(default=False, nullable=False)


# class User(SQLAlchemyBaseUserTable[int], Base):
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False)
#     username = Column(String, nullable=False)
#     registered_at = Column(TIMESTAMP, default=datetime.utcnow)
#     hashed_password: str = Column(String(length=1024), nullable=False)
#     is_active: bool = Column(Boolean, default=True, nullable=False)
#     is_superuser: bool = Column(Boolean, default=False, nullable=False)
#     is_verified: bool = Column(Boolean, default=False, nullable=False)
#
#     posts = relationship("Post", back_populates="user")

    # __mapper_args__ = {"eager_defaults": True}

# async def get_user_db(session: AsyncSession = Depends(get_db_session)):
#     yield SQLAlchemyUserDatabase(session, User)
user_db = OrmarUserDatabase(UserDB, User)
