from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.services import user_service
from app.schemas.user import UserResponse, UserCreate, UserUpdate, UserLogin
from dependencies.auth import require_role, get_current_user
from app.models.db_models import UserDB

user_router = APIRouter()


@user_router.post("/create", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    new_user = user_service.register_user(db, user)
    return new_user


@user_router.get("/show", response_model=list[UserResponse])
def show_all_users(
    db: Session = Depends(get_db), current_user: UserDB = Depends(require_role("admin"))
) -> list[UserResponse]:
    users = user_service.select_all_users(db)
    return users


@user_router.get("/show/{id}", response_model=UserResponse)
def show_usere_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_role("admin")),
) -> UserResponse:
    user = user_service.select_user_by_id(db, id)
    return user


@user_router.delete("/delete/{id}")
def delete_user_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_role("admin")),
) -> dict:
    user_service.delete_user_by_id(db, id)

    return {"message": "user deleted successfully"}


@user_router.put("/update/{id}", response_model=UserResponse)
def update_user_by_id(
    id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(require_role("admin")),
) -> UserResponse:
    updating_user = user_service.user_update(db, id, user)

    return updating_user


@user_router.post("/login")
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict | None:
    user = UserLogin(identifier=form_data.username, password=form_data.password)
    token = user_service.user_login(user, db)
    return {"access_token": token, "token_type": "bearer"}


@user_router.get("/user/me", response_model=UserResponse)
def show_my_informatin(
    db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)
):
    user = user_service.select_user_by_id(db, current_user.id)
    return user
