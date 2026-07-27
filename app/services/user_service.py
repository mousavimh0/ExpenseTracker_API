from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.repositories import user_repository
from app.models.db_models import UserDB
from fastapi import HTTPException

def register_user(db : Session, user :UserCreate):
    user_by_email = user_repository.get_user_by_email(db , user.email)
    user_by_username = user_repository.get_user_by_username(db, user.username)

    if user_by_email:
        raise HTTPException(409, "Email already exist")
    elif user_by_username:
        raise HTTPException(409, "Username already exist")

    new_user = user_repository.create_user(db, user)
    return new_user