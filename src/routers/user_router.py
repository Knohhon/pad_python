from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserAuth
from crud.user_crud import get_user_by_email, get_user_by_username, create_user, user_auth
from database.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):

    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )

    new_user = create_user(db, user)
    return new_user