from sqlalchemy.orm import Session
from src.database.database_models import User
from src.schemas.user import UserCreate, UserAuth
from src.utils.security import get_password_hash, verify_password


def user_auth(db: Session, user: UserAuth):
    current_user = get_user_by_email(db, user)
    if verify_password(user.password, current_user.hashed_password):
        return current_user        

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role="user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user