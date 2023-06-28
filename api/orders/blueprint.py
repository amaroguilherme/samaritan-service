from flask import Blueprint, jsonify, request

from api.orders.models import Order
from api.users.models import User

orders = Blueprint('orders', __name__)

@orders.route('/create', methods=['POST'])
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
        return jsonify(dict(message="Change this message")), 500
    
    return jsonify(dict(message="Order created")), 200

@orders.route('/get/<id>', methods=['GET'])
def get(id):
    try:
        current_order = Order.get(
            _id=id
        )
        
    except:
        return jsonify(dict(message="Change this message")), 500
    
    return jsonify(current_order), 200

@orders.route('/update/<id>', methods=['PATCH'])
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
        return jsonify(dict(message="Change this message")), 500

    return jsonify(dict(message="Order updated")), 200

@orders.route('/list', methods=['GET'])
def list():
    try:
        orders = Order.list()

    except:
        return jsonify(dict(message="Change this message")), 500

    return jsonify(dict(orders=orders)), 200

@orders.route('delete/<id>', methods=['DELETE'])
def delete(id):
    try:
        Order.delete(id)

    except:
        return jsonify(dict(message="Change this message")), 500

    return jsonify(dict(message="Order deleted")), 200

@orders.route('close/<id>', methods=['PATCH'])
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
        return jsonify(dict(message="Change this message")), 500

    return jsonify(dict(message="Transaction completed")), 200