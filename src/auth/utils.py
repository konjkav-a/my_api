from typing import Any
from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config
import jwt
import uuid
import logging


passwd_context = CryptContext(schemes=["bcrypt"])
ACCESS_TOKEN_EXPIRY = 3600


def generate_passwd_hash(password: str) -> str:
    hash_pass = passwd_context.hash(password)

    return hash_pass


def verify_password(password: str, hash_pass: str) -> bool:
    return passwd_context.verify(password, hash_pass)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):

    payload = {'user': user_data,
               'exp': datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))}

    """ This is a unique identifier for the token. It’s a string that uniquely distinguishes 
        each token from others.
    """
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(payload=payload,key=Config.JWT_SECRET,algorithm=Config.JWT_ALGORITHM)

    return token

def decode_token(token: str) -> Any | None:
    try:
        token_data = jwt.decode(jwt= token,key=Config.JWT_SECRET,algorithms=[Config.JWT_ALGORITHM])
        # print(token_data)
        return token_data

    except jwt. PyJWTError as e:
        logging.exception(e)
        return None
