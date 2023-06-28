from functools import wraps
from hashlib import sha256
import random
import datetime
from flask import jsonify, request
import jwt
from storage.config import SECRET_KEY

def encode(string):
    encoded_string = string.encode('utf-8')

    h = sha256()
    h.update(encoded_string)

    salt = str(random.random()).split(".")[1]

    return {
        "hash": h.hexdigest(),
        "salt": salt
    }

def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

def decode_auth_token(func):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            jwt.decode(request.headers['Authorization'].split('Bearer ')[1], SECRET_KEY, algorithms=["HS256"])
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(dict(message='Signature expired. Please log in again.')), 401
        except jwt.InvalidTokenError:
            return jsonify(dict(message='Invalid token. Please log in again.')), 401
        
    return wrapper