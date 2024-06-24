import typing

from db import db_user
from models import User
from utils import encrypt_password, decrypt_password, create_access_token


def register(username: str, raw_password: str) -> typing.Optional[bool, dict]:
    fetch_response = db_user.fetch({'username': username})
    if fetch_response.count != 0:
        return False

    return db_user.put({'username': username, 'password': encrypt_password(raw_password)})


def login(username: str, password: str) -> typing.Optional[bool, str]:
    fetch_response = db_user.fetch({'username': username})
    if fetch_response.count == 0:
        return False

    user = User(**fetch_response.items[0])
    if decrypt_password(user.password) == password:
        return create_access_token({'username': username})

    return False


