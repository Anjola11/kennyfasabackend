from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from src.config import Config

password_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password:str) -> str:
    password_hash = password_context.hash(password)

    return password_hash

def verify_password_hash(password:str, pasword_hash:str):
    password_valid = password_context.verify(password, pasword_hash)

    return password_valid

def create_user_access_token(user_data:dict, expiry: timedelta = None) -> str:
    payload = {
        'sub': user_data['id'],
        'user': user_data,
        'type': 'access',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() +expiry
    }

    token = jwt.encode(
        payload= payload,
        key = Config.JWT_KEY,
        algorithm= Config.JWT_ALGORITHM
    )

    return token

def create_user_refresh_token(user_data_id: str, expiry: timedelta=None) -> str:
    payload ={
        'sub': user_data_id,
        'type': 'refresh',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() +expiry
    }

    token = jwt.encode(
        payload= payload,
        key = Config.JWT_KEY,
        algorithm= Config.JWT_ALGORITHM
    )

    return token

def decode_user_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        key = Config.JWT_KEY,
        algorithms=[Config.JWT_ALGORITHM]
    )

    return payload

def create_admin_access_token(admin_data: dict, expiry: timedelta= None) -> str:
    payload = {
        'sub': admin_data['id'],
        'admin': admin_data,
        'type': 'access',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + expiry
    }

    token = jwt.encode(
        payload=payload,
        key= Config.JWT_KEY,
        algorithm= Config.JWT_ALGORITHM
    )

    return token

def create_admin_refresh_token(admin_data_id: dict, expiry: timedelta=None) -> str:
    payload = {
        'sub': admin_data_id,
        'type': 'refresh',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + expiry,
    }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_KEY,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_admin_token(token):
    payload = jwt.decode(
        token,
        key=Config.JWT_KEY,
        algorithms=[Config.JWT_ALGORITHM]
    )

    return payload
