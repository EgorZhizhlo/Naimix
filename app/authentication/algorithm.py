import bcrypt
from jose import jwt, JWTError
import datetime as dt
from app.core import secret_key, algorithm
from .dao import UserDAO


async def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


async def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


async def create_access_token(data: dict):
    to_encode = data.copy()
    date_now = dt.datetime.now(dt.UTC)
    expire = date_now + dt.timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm)
    return encoded_jwt


async def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        return payload
    except JWTError:
        return None


async def authenticate_user(email: str, password: str):
    user = await UserDAO.find(
        all=False,
        or_method=False,
        email=email
    )

    if user:
        verify_flag = await verify_password(
            password=password,
            hashed_password=user.password
        )
        if verify_flag:
            return user
    return None
