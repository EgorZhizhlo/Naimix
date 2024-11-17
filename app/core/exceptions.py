from fastapi import status, HTTPException


class TokenExpiredException(HTTPException):
    '''
    TokenExpiredException:
     Исключение, вызываемое при истечении срока действия токена (HTTP 401).
    '''
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен истек!'
        )


class TokenNoFoundException(HTTPException):
    '''
    TokenNoFoundException:
     Исключение, вызываемое при отсутствии токена (HTTP 401).
    '''
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен не найден!'
        )


class UserAlreadyExistsException(HTTPException):
    '''
    UserAlreadyExistsException:
    Исключение, вызываемое при попытке создать пользователя,
     который уже существует (HTTP 409).
    '''
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует!'
        )


class PasswordMismatchException(HTTPException):
    '''
    PasswordMismatchException:
     Исключение, вызываемое при несовпадении паролей (HTTP 409).
    '''
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пароли не совпадают!'
        )


class IncorrectEmailOrPasswordException(HTTPException):
    '''
    IncorrectEmailOrPasswordException:
     Исключение, вызываемое при неверной почте или пароле (HTTP 401).
    '''
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная электронная почта или пароль!',
        )


class IncorrectFormatException(HTTPException):
    '''
    IncorrectEmailOrPasswordException:
    Исключение, вызываемое при неверной валидаци значений (HTTP 401).
    '''
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный формат вводимых данных!'
        )


class NoJwtException(HTTPException):
    '''
    NoJwtException:
     Исключение, вызываемое при отсутствии или
     недействительности токена (HTTP 401).
    '''
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен не валидный!'
        )


class NoUserIdException(HTTPException):
    '''
    NoUserIdException:
     Исключение, вызываемое при отсутствии ID пользователя (HTTP 401).
    '''
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь не найден!'
        )


class ForbiddenException(HTTPException):
    '''
    ForbiddenException:
     Исключение, вызываемое при недостатке прав доступа (HTTP 403).
    '''
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав!'
        )
