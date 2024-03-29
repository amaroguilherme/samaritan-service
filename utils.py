from functools import wraps
from hashlib import sha256

import random
import datetime
import json

from flask import jsonify, request
import jwt
from api.orders.models import Order
from api.users.models import User
from storage.base import db_session
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
        
@staticmethod
def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def validate_auth_token(func):
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

def validate_fields(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        blacklisted_items = ["total_amount"]
        if all(item not in blacklisted_items for item in request.form.keys()):
            return func(*args, **kwargs)
            
        else:
            return jsonify(dict(message='Some fields are not allowed. Please review it and try again.')), 400
        
    return wrapper

def validate_balance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        buyer_id = decode_auth_token(request.headers['Authorization'].split('Bearer ')[1])

        order = Order.get(
            kwargs['id']
        )
        
        buyer = (
                db_session.query(User)
                    .filter(User.id == buyer_id)
                    .first()
            )

        if buyer.total_amount >= order['amount'] or int(order['owner_id']) == buyer_id:
            return func(*args, **kwargs)
            
        else:
            return jsonify(dict(message='User does not have enough balance to complete this transaction.')), 400
        
    return wrapper