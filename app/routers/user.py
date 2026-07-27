from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserCreate
from app.services import user_service

user_router = APIRouter()

@user_router.post("/", response_model=UserResponse, status_code=201)
def create_user(user : UserCreate ,db : Session =Depends(get_db)):
    new_user = user_service.register_user(db , user)
    return new_user