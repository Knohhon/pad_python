from fastapi import FastAPI
from database import Base, engine
from auth_router import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Registration API",
    description="API для регистрации пользователей",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API регистрации пользователей!"}