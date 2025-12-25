import uvicorn
from fastapi import FastAPI
from fastapi import Depends
from src.database.database_models import Base, engine
from src.routers.user_router import router as user_router
from src.routers.question_router import router as question_router
from src.routers.tests_router import router as test_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Registration API",
    description="API для регистрации пользователей",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(test_router)
app.include_router(question_router)

@app.get("/")
async def root():
    return {"message": "Knowledge testing app"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__=='__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port='8000'
    )