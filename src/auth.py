import hashlib
from functools import singledispatch
from typing import Optional

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import Session

from models import TableBooking, User

SALT = "STRONg@Salt"
SECRET_KEY = "!SECRET!"
TOKEN_EXPIRES_IN = 3600 * 24 * 30


@singledispatch
def authorize(instance, current_user: User) -> bool:
    raise NotImplementedError


@authorize.register(TableBooking)
def _authorize(instance: TableBooking, current_user: User) -> bool:
    return instance.user_id == current_user.id


def generate_password_hash(password: str) -> str:
    h = hashlib.md5(f"{password}{SALT}".encode())
    return h.hexdigest()


def verify_password(user: User, password: str) -> bool:
    return user.password == generate_password_hash(password)


def generate_token(user: User) -> str:
    serializer = Serializer(SECRET_KEY, expires_in=TOKEN_EXPIRES_IN)
    return serializer.dumps({"user_id": user.id}).decode("utf-8")


def get_user_by_token(session: Session, token: str) -> Optional[User]:
    serializer = Serializer(SECRET_KEY, expires_in=TOKEN_EXPIRES_IN)
    data = serializer.loads(token)
    return session.query(User).get(data["user_id"])
