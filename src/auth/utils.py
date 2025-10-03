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

def create_access_token(user_data:dict, expiry: timedelta) -> str:
    payload = {
        'sub': user_data.id,
        'user': user_data,
        'exp': datetime.utcnow +expiry,
        'iat': datetime.utcnow
    }

    token = jwt.encode(
        payload= payload,
        key = Config.JWT_KEY,
        algorithm= Config.JWT_ALGORITHM
    )

    return token