from flask import Blueprint, jsonify, request
from storage.base import db_session
from api.users.models import User, UserProfile
from utils import encode, encode_auth_token, decode_auth_token

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
        return jsonify(dict(message="Username is already in use")), 400

    encoded_password = encode(request.form.get('password'))

    try:
        current_user = User.add(
            _username=username,
            _password=encoded_password["hash"],
            _salt=encoded_password["salt"],
            _total_amount=0.00,
            _contributions=0,
            db_session=db_session
        )

        user_profile = UserProfile.add(
            _user_id=current_user.id,
        )
    
        auth_token = encode_auth_token(current_user.id)

        return jsonify(dict(user=username, data="User Added", auth_token=auth_token)), 200
    
    except:
        return jsonify(dict(message="Change this message")), 500
    
@users.route('/update/user/<id>', methods=['PATCH'])
@decode_auth_token
def update_user(id):
    fields = request.form
    try:
        for field in fields:
            User.update(
                id,
                {
                    field: fields.get(field)
                }
            )

    except Exception as e:
        return jsonify(dict(message="Change this message")), 500

    return jsonify(dict(message="User Profile updated")), 200

@users.route('/update/balance/<id>', methods=['PATCH'])
@decode_auth_token
def update_balance(id):
    amount = float(request.form.get('amount'))

    try:
        user = User.get(
            id
        )

        updated_balance = user.total_amount + amount

        User.update(
            id,
            {
                "total_amount": updated_balance
            }
        )

    except Exception as e:
        return jsonify(dict(message="Change this message")), 500

    return jsonify(dict(message="User Profile updated")), 200


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

    except:
        return jsonify(dict(message="Change this message")), 500