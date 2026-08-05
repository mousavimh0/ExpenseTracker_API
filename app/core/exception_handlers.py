from fastapi import Request
from fastapi.responses import JSONResponse


from app.core.expetions import (
    NotFoundException,
    PermissionException,
    AuthenticationException,
    AlreadyExistException,
)


async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404, content={"error": exc.error, "message": exc.message}
    )


async def permission_handler(request: Request, exc: PermissionException):
    return JSONResponse(
        status_code=403, content={"error": exc.error, "message": exc.message}
    )


async def autentication_handler(request: Request, exc: AuthenticationException):
    return JSONResponse(
        status_code=401, content={"error": exc.error, "message": exc.message}
    )


async def already_exist_handler(request: Request, exc: AlreadyExistException):
    return JSONResponse(
        status_code=409, content={"error": exc.error, "message": exc.message}
    )
