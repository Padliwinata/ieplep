import typing
from datetime import datetime, timedelta

from cryptography.fernet import Fernet
import streamlit as st
from jose import jwt

f = Fernet(st.secrets['SECRET_KEY'])


def encrypt_password(raw_password: str) -> str:
    encoded_password = raw_password.encode('utf-8')
    encrypted_password = f.encrypt(encoded_password).decode('utf-8')
    return encrypted_password


def decrypt_password(password: str) -> str:
    return f.decrypt(password).decode('utf-8')


def create_access_token(data: typing.Dict[str, typing.Any]) -> str:
    to_encode = data.copy()
    to_encode.update(
        {'exp': datetime.now() + timedelta(seconds=st.secrets['SECRET_KEY']), 'iat': datetime.now()})
    encoded_jwt = jwt.encode(to_encode, st.secrets['SECRET_KEY'], algorithm=st.secrets['ALGORITHM'])
    return encoded_jwt

