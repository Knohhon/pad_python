import uvicorn
from fastapi import FastAPI
from fastapi import Depends
from database.database import Base, engine
from routers.user_router import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Registration API",
    description="API для регистрации пользователей",
    version="1.0.0"
)

app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Knowledge testing app"}


if __name__=='__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port='8000'
    )