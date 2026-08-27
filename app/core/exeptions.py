class NotFoundException(Exception):
    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message


class PermissionException(Exception):
    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message


class AuthenticationException(Exception):
    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message


class AlreadyExistException(Exception):
    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message


class ExpiredTokenException(Exception):
    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message


class InvalidTokenException(Exception):
    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message
