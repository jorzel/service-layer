import re
from functools import wraps

from graphene.relay.node import from_global_id

from auth import authorize, get_user_by_token
from models import User


def camel_to_snake(name: str) -> str:
    """CamelCase -> camel_case"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class UnauthenticatedUser(Exception):
    pass


class UnauthorizedAccess(Exception):
    pass


class InstanceNotExist(Exception):
    pass


def authorize_required(model):
    """
    We assume that global id field name of resource followe convention like:
    model_name: TableBooking
    global id field name: table_booking_gid
    """

    def decorator(func):
        @wraps(func)
        def wrapper(root, info, *args, **kwargs):
            kwargs["current_user"] = get_current_user(info.context)
            model_name = model.__name__
            gid_field_name = f"{camel_to_snake(model_name)}_gid"
            instance_gid = kwargs[gid_field_name]
            instance_model_name, instance_id = from_global_id(instance_gid)
            if instance_model_name != f"{model_name}Node":
                raise UnauthorizedAccess()
            instance = info.context["session"].query(model).get(instance_id)
            if not instance:
                InstanceNotExist()
            kwargs["instance"] = instance
            if not authorize(instance, kwargs["current_user"]):
                raise UnauthorizedAccess()
            return func(root, info, *args, **kwargs)

        return wrapper

    return decorator


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
