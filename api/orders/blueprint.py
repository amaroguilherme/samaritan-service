from flask import Blueprint, jsonify, request

from api.orders.models import Order
from utils import decode_auth_token

orders = Blueprint('orders', __name__)

@orders.route('/create', methods=['POST'])
@decode_auth_token
def create():
    username = request.form.get('username')
    description = request.form.get('description')
    amount = request.form.get('amount')

    try:
        Order.add(
            _owner_name=username,
            _description=description,
            _amount=amount,
            _is_active=True
        )
    
    except Exception as e:
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500
    
    return jsonify(dict(message=f"A order was created for the user {username}")), 200

@orders.route('/get/<id>', methods=['GET'])
@decode_auth_token
def get(id):
    try:
        current_order = Order.get(
            _id=id
        )
        
    except:
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500
    
    return jsonify(dict(order=current_order)), 200

@orders.route('/update/<id>', methods=['PATCH'])
@decode_auth_token
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
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

    return jsonify(dict(message=f"The order of id number {id} was updated.")), 200

@orders.route('/list', methods=['GET'])
@decode_auth_token
def list():
    try:
        orders = Order.list()

    except:
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

    return jsonify(dict(orders=orders)), 200

@orders.route('delete/<id>', methods=['DELETE'])
@decode_auth_token
def delete(id):
    try:
        Order.delete(id)

    except:
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

    return jsonify(dict(message=f"The order of id number {id} was deleted")), 200

@orders.route('close/<id>', methods=['PATCH'])
@decode_auth_token
def close(id):
    buyer_name = request.form.get('buyer_name')
    fields = {
                "buyer_name": buyer_name,
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
        return jsonify(dict(message="Something went wrong. Please, reach out support for further assistance.")), 500

    return jsonify(dict(message=f"The order of id number {id} was completed")), 200