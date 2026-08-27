from pydantic import BaseModel, ConfigDict
from app.schemas.transaction import TransactionResponse
from enum import Enum


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    transactions: list[TransactionResponse]
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str
    email: str
    role: UserRole


class UserLogin(BaseModel):
    identifier: str
    password: str
