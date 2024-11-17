from app.core import BaseDAO
from .models import User


class UserDAO(BaseDAO):
    model = User
