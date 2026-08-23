from fastapi import FastAPI


from app.routers.transactions import transaction_router
from app.routers.report import report_router
from app.database import engine, Base
from app.models import db_models
from app.routers.user import user_router
from app.core.expetions import (
    NotFoundException,
    PermissionException,
    AuthenticationException,
    AlreadyExistException,
    ExpiredTokenException,
    InvalidTokenException,
)
from app.core.exception_handlers import (
    not_found_handler,
    permission_handler,
    autentication_handler,
    already_exist_handler,
    expierd_token_handler,
    invalid_token_handler,
)

app = FastAPI()

app.add_exception_handler(NotFoundException, not_found_handler)
app.add_exception_handler(PermissionException, permission_handler)
app.add_exception_handler(AuthenticationException, autentication_handler)
app.add_exception_handler(AlreadyExistException, already_exist_handler)
app.add_exception_handler(ExpiredTokenException, expierd_token_handler)
app.add_exception_handler(InvalidTokenException, invalid_token_handler)


app.include_router(router=transaction_router, prefix="/transactions")
app.include_router(router=report_router, prefix="/report")
app.include_router(router=user_router, prefix="/users")
