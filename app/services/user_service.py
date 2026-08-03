from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.db_models import UserDB
from app.repositories import user_repository
from app.schemas.user import UserCreate, UserUpdate, UserLogin
from app.core import security


def register_user(db: Session, user: UserCreate) -> UserDB | None:
    user_by_email = user_repository.get_user_by_email(db, user.email)
    user_by_username = user_repository.get_user_by_username(db, user.username)

    if user_by_email:
        raise HTTPException(409, "Email already exist")
    elif user_by_username:
        raise HTTPException(409, "Username already exist")

    hashed_password = security.hash_password(user.password)
    user.password = hashed_password
    new_user = user_repository.create_user(db, user)
    return new_user


def select_all_users(
    db: Session,
) -> list[UserDB] | None:
    users = user_repository.get_all_users(db)
    if users:
        return users
    else:
        raise HTTPException(404, "users not found.")


def select_user_by_id(db: Session, user_id) -> UserDB | None:
    user = user_repository.get_user_by_id(db, user_id)
    if user:
        return user
    else:
        raise HTTPException(404, "user not found")


def delete_user_by_id(db: Session, id: int) -> None:
    select_user_by_id(db, id)
    user_repository.delete_user_by_id(db, id)


def user_update(db: Session, id: int, user: UserUpdate) -> UserDB | None:
    select_user_by_id(db, id)
    updated_user = user_repository.update_user_by_id(db, id, user)
    return updated_user


def user_login(user: UserLogin, db: Session) -> bool:
    if "@" in user.identifier:
        current_user = user_repository.get_user_by_email(db, user.identifier)
        if not current_user:
            raise HTTPException(401, "Invalid username/email or password")
    else:
        current_user = user_repository.get_user_by_username(db, user.identifier)
        if not current_user:
            raise HTTPException(401, "Invalid username/email or password")

    if security.verify_password(user.password, current_user.hashed_password):
        token = security.create_access_token({"sub": str(current_user.id)})
        return token
    else:
        raise HTTPException(401, "Invalid username/email or password")
