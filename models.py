from pydantic import BaseModel
from utils import encrypt_password


class User(BaseModel):
    username: str
    password: str

    def set_password(self, raw_password: str):
        self.password = encrypt_password(raw_password)

