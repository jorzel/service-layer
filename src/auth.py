import hashlib

SALT = "STRONg@Salt"


def generate_password_hash(password: str) -> str:

    h = hashlib.md5(f"{password}{SALT}".encode())
    return h.hexdigest()
