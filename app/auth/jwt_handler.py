import time 
import jwt
from decouple import config 

JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')


def token_response(token: str) -> dict:
    return {
        'access_token': token,
        'token_type': 'bearer'
    }

def sign_jwt(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': time.time() + 60000  # Token expires in 1000 minutes
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")