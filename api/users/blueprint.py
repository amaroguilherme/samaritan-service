import logging

from flask import Blueprint, jsonify, request
from api.orders.models import Order
from storage.base import db_session
from api.users.models import User
from utils import encode, encode_auth_token, decode_auth_token, validate_auth_token, validate_fields

log = logging.getLogger()
log.setLevel(logging.INFO)

users = Blueprint('users', __name__)

@users.route('/create', methods=['POST'])
def create():
    username = request.form.get('username')

    current_user = (
                db_session.query(User)
                    .filter(User.username == username)
                    .first()
            )

    if current_user:
        return jsonify(dict(message=f"A user called {username} already exists.")), 400

    encoded_password = encode(request.form.get('password'))

    try:
        current_user = User.add(
            _username=username,
            _password=encoded_password["hash"],
            _salt=encoded_password["salt"],
            _total_amount=0.00,
            db_session=db_session
        )
    
        auth_token = encode_auth_token(current_user.id)

        return jsonify(dict(message=f"A user named {username} was created.", auth_token=auth_token)), 200
    
    except Exception as e:
        log.exception(e)
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500
    
@users.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = encode(request.form.get('password'))["hash"]

    try:
        user = (
                db_session.query(User)
                    .filter(User.username == username)
                        .first()
            )
        if user and (password + user.salt) == (user.password + user.salt):
            auth_token = encode_auth_token(user.id)
            if auth_token:
                return jsonify(message='Login Successful', auth_token=auth_token), 200
        else:
            return jsonify(dict(message="Unauthorized")), 401

    except Exception as e:
        log.exception(e)
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

@users.route('/update/user', methods=['PATCH'])
@validate_auth_token
@validate_fields
def update_user():
    user_id = decode_auth_token(request.headers['Authorization'].split('Bearer ')[1])
    fields = request.form

    try:
        for field in fields:
            User.update(
                user_id,
                {
                    field: fields.get(field)
                }
            )

    except Exception as e:
        log.exception(e)
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

    return jsonify(dict(message=f"The requested fields for the user with id number {user_id} was updated.")), 200

#TODO: THIS SHOULD VERIFY FIRST IF THE BUYER HAS ENOUGH BALANCE TO COMPLETE THE TRANSACTION
@users.route('/update/balance', methods=['PATCH'])
@validate_auth_token
def update_balance():
    user_id = decode_auth_token(request.headers['Authorization'].split('Bearer ')[1])
    order_id = request.form.get('order_id')

    try:
        order = Order.get(
            order_id
        )
        
        buyer = (
                db_session.query(User)
                    .filter(User.id == order['buyer_id'] and user_id == order['buyer_id'])
                    .first()
            )
        
        owner = (
                db_session.query(User)
                    .filter(User.id == order['owner_id'])
                    .first()
            )
        
        buyer_updated_balance = buyer.total_amount - order['amount']
        owner_updated_balance = owner.total_amount + order['amount']

        User.update(
            order['buyer_id'],
            {
                "total_amount": buyer_updated_balance
            }
        )

        User.update(
            order['owner_id'],
            {
                "total_amount": owner_updated_balance
            }
        )

    except Exception as e:
        log.exception(e)
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

    return jsonify(dict(message=f"The balance for the user with id number {user_id} was updated")), 200