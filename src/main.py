from fastapi import FastAPI, Depends


from src.routes import routes
from src.core.db import database, metadata, engine
from src.redis import redis_session

app = FastAPI()

metadata.create_all(engine)
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    redis_session()
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(routes)
