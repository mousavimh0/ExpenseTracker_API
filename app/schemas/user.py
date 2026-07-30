from pydantic import BaseModel, ConfigDict
from app.schemas.transaction import TransactionResponse


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    transactions: list[TransactionResponse]

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str
    email: str


class UserLogin(BaseModel):
    identifier: str
    password: str
