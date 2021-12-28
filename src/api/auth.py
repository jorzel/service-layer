from functools import wraps

from auth import get_user_by_token
from models import User


class UnauthenticatedUser(Exception):
    pass


def sign_in_required():
    def decorator(func):
        @wraps(func)
        def wrapper(root, info, *args, **kwargs):
            kwargs["current_user"] = get_current_user(info.context)
            return func(root, info, *args, **kwargs)

        return wrapper

    return decorator


def get_current_user(context) -> User:
    try:
        token = get_token_from_request(context["request"])
        user = get_user_by_token(context["session"], token)
        if not user:
            raise UnauthenticatedUser("UnauthenticatedUser")
        return user
    except KeyError:
        raise UnauthenticatedUser("UnauthenticatedUser")


def get_token_from_request(request):
    header = request.headers["Authorization"]
    token = header.replace("Bearer ", "", 1)
    return token
