import logging

from flask import Blueprint, jsonify, request

from api.orders.models import Order
from utils import decode_auth_token, validate_auth_token

log = logging.getLogger()
log.setLevel(logging.INFO)

orders = Blueprint('orders', __name__)

@orders.route('/create', methods=['POST'])
@validate_auth_token
def create():
    user_id = decode_auth_token(request.headers['Authorization'].split('Bearer ')[1])
    description = request.form.get('description')
    amount = request.form.get('amount')

    try:
        Order.add(
            _owner_id=user_id,
            _description=description,
            _amount=amount,
            _is_active=True
        )
    
    except Exception as e:
        log.exception(e)
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500
    
    return jsonify(dict(message=f"A order was created for the user with id number {user_id}")), 200

@orders.route('/get/<id>', methods=['GET'])
@validate_auth_token
def get(id):
    try:
        current_order = Order.get(
            _id=id
        )
        
    except Exception as e:
        log.exception(e)
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500
    
    return jsonify(dict(order=current_order)), 200

@orders.route('/update/<id>', methods=['PATCH'])
@validate_auth_token
def update(id):
    fields = request.form
    try:
        for field in fields:
            Order.update(
                id,
                {
                    field: fields.get(field)
                }
            )

    except Exception as e:
        log.exception(e)
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

    return jsonify(dict(message=f"The order of id number {id} was updated.")), 200

@orders.route('/list', methods=['GET'])
@validate_auth_token
def list():
    try:
        orders = Order.list()

    except Exception as e:
        log.exception(e)
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

    return jsonify(dict(orders=orders)), 200

@orders.route('delete/<id>', methods=['DELETE'])
@validate_auth_token
def delete(id):
    try:
        Order.delete(id)

    except Exception as e:
        log.exception(e)
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

    return jsonify(dict(message=f"The order of id number {id} was deleted")), 200

#TODO: THIS SHOULD NULLIFY BUYER_ID IF THE OWNER CLOSES THE ORDER
#TODO: THIS SHOULD VERIFY FIRST IF THE BUYER HAS ENOUGH BALANCE TO COMPLETE THE TRANSACTION
#TODO: ADD TESTS TO THIS ROUTE
@orders.route('close/<id>', methods=['PATCH'])
@validate_auth_token
def close(id):
    buyer_id = decode_auth_token(request.headers['Authorization'].split('Bearer ')[1])
    fields = {
                "buyer_id": buyer_id,
                "is_active": False
            }
    try:
        for field in fields:
            Order.update(
                id,
                {
                    field: fields.get(field)
                }
            )
        
    except Exception as e:
        log.exception(e)
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

    return jsonify(dict(message=f"The order of id number {id} was completed")), 200