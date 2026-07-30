from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.core import security
from app.database import get_db
from app.repositories import user_repository
from app.core import security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = security.decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(401, "inavalid token")
    current_user = user_repository.get_user_by_id(db, int(user_id))

    return current_user
