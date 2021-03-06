from fastapi import FastAPI
from routers import account, music
from sql_app.database import SessionLocal, engine
from sql_app import models


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(account.router)
app.include_router(music.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

