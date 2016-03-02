import uuid

import pyscrypt


def make_hash(password: str, salt=None) -> tuple:
    if salt:
        if isinstance(salt, str):
            salt = bytes(salt, encoding='utf-8')
    else:
        salt = uuid.uuid4().bytes
    return pyscrypt.hash(bytes(password, encoding='utf-8'), salt, 1024, 2, 2, 128), salt


def check_password(password, password_hash, salt):
    return password_hash == make_hash(password, salt)[0]
