from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.db_models import UserDB
from app.schemas.user import UserCreate, UserUpdate


def get_user_by_email(db: Session, email: str) -> UserDB | None:
    statement = select(UserDB).where(UserDB.email == email)
    user = db.execute(statement).scalar_one_or_none()

    return user


def get_user_by_username(db: Session, username: str) -> UserDB | None:
    statement = select(UserDB).where(UserDB.username == username)
    user = db.execute(statement).scalar_one_or_none()

    return user


def create_user(db: Session, user: UserCreate) -> UserDB:
    new_user = UserDB(
        username=user.username, email=user.email, hashed_password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session) -> list[UserDB] | None:
    statement = select(UserDB)
    users = db.execute(statement).scalars().all()
    return users


def get_user_by_id(db: Session, user_id) -> UserDB | None:
    statement = select(UserDB).where(UserDB.id == user_id)
    user = db.execute(statement).scalar_one_or_none()
    return user


def delete_user_by_id(db: Session, id: int) -> None:
    user = get_user_by_id(db, id)
    db.delete(user)
    db.commit()


def update_user_by_id(db: Session, id: int, user: UserUpdate):
    updating_user = get_user_by_id(db, id)
    updating_user.username = user.username
    updating_user.email = user.email
    updating_user.role = user.role
    db.commit()
    db.refresh(updating_user)
    return updating_user
