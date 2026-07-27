from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.db_models import UserDB
from typing import Optional
from app.schemas.user import UserCreate

def get_user_by_email(db : Session, email : str)-> Optional[UserDB]:
    statement = select(UserDB).where(UserDB.email == email)
    user = db.execute(statement).scalar_one_or_none()

    return user


def get_user_by_username(db : Session, username : str)-> Optional[UserDB]:
    statement = select(UserDB).where(UserDB.username == username)
    user = db.execute(statement).scalar_one_or_none()

    return user

def create_user(db : Session, user : UserCreate )-> UserDB:
    new_user = UserDB(username = user.username, email = user.email, hashed_password = user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
