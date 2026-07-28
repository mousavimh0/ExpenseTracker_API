from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import user_service
from app.schemas.user import UserResponse, UserCreate, UserUpdate


user_router = APIRouter()


@user_router.post("/create", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    new_user = user_service.register_user(db, user)
    return new_user


@user_router.get("/show", response_model=list[UserResponse])
def show_all_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    users = user_service.select_all_users(db)
    return users


@user_router.get("/show/{id}", response_model=UserResponse)
def show_usere_by_id(id: int, db: Session = Depends(get_db)) -> UserResponse:
    user = user_service.select_user_by_id(db, id)
    return user


@user_router.delete("/delete/{id}")
def delete_user_by_id(id: int, db: Session = Depends(get_db)) -> dict:
    user_service.delete_user_by_id(db, id)

    return {"message": "user deleted successfully"}


@user_router.put("/update/{id}", response_model=UserResponse)
def update_user_by_id(
    id, user: UserUpdate, db: Session = Depends(get_db)
) -> UserResponse:
    updating_user = user_service.user_update(db, id, user)

    return updating_user
