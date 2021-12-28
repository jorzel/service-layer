from auth import get_user_by_token
from models import User


class UnauthenticatedUser(Exception):
    pass


def get_current_user(context) -> User:
    try:
        token = get_token_from_request(context["request"])
        user = get_user_by_token(context["session"], token)
        if not user:
            raise UnauthenticatedUser()
        return user
    except KeyError:
        raise UnauthenticatedUser()


def get_token_from_request(request):
    header = request.headers["Authorization"]
    token = header.replace("Bearer ", "", 1)
    return token
