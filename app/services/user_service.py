from sqlalchemy.orm import Session


from app.models.db_models import UserDB
from app.repositories import user_repository
from app.schemas.user import UserCreate, UserUpdate, UserLogin
from app.core import security
from app.core.expetions import (
    AuthenticationException,
    NotFoundException,
    AlreadyExistException,
)


def register_user(db: Session, user: UserCreate) -> UserDB | None:
    user_by_email = user_repository.get_user_by_email(db, user.email)
    user_by_username = user_repository.get_user_by_username(db, user.username)

    if user_by_email:
        raise AlreadyExistException("Already exist", "Email already exist")
    elif user_by_username:
        raise AlreadyExistException("Already exist", "Username already exist")

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
        raise NotFoundException("Not found", "User not found")


def select_user_by_id(db: Session, user_id) -> UserDB | None:
    user = user_repository.get_user_by_id(db, user_id)
    if user:
        return user
    else:
        raise NotFoundException("Not found", "User not found")


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
            raise AuthenticationException(
                "Authentication faild", "Wrong password or email"
            )
    else:
        current_user = user_repository.get_user_by_username(db, user.identifier)
        if not current_user:
            raise AuthenticationException(
                "Authentication faild", "Wrong password or email"
            )

    if security.verify_password(user.password, current_user.hashed_password):
        token = security.create_access_token(
            {"sub": str(current_user.id), "role": current_user.role}
        )
        return token
    else:
        raise AuthenticationException("Authentication faild", "Wrong password or email")
