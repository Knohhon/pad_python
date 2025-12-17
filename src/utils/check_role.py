from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.models import User
from security import get_current_user

async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут создавать тесты"
        )
    return current_user