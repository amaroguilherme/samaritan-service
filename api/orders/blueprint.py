import json
import logging

from flask import Blueprint, jsonify, redirect, render_template, request
import stripe

from storage.base import db_session
from api.users.models import User
from api.orders.models import Order
from utils import decode_auth_token, validate_auth_token, validate_balance

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

@orders.route('close/<id>', methods=['PATCH'])
@validate_auth_token
@validate_balance
def close(id):
    buyer_id = decode_auth_token(request.headers['Authorization'].split('Bearer ')[1])
    fields = dict(is_active=False)

    try:
        order = (
                db_session.query(Order)
                    .filter(Order.id == id and Order.is_active == True)
                    .first()
            )

        if order.buyer_id != order.owner_id:

            buyer = (
                db_session.query(User)
                    .filter(User.id == buyer_id)
                    .first()
            )
        
            owner = (
                    db_session.query(User)
                        .filter(User.id == order.owner_id)
                        .first()
                )
            
            buyer_updated_balance = buyer.total_amount - order.amount
            owner_updated_balance = owner.total_amount + order.amount

            User.update(
                order.buyer_id,
                {
                    "total_amount": buyer_updated_balance
                }
            )

            User.update(
                order.owner_id,
                {
                    "total_amount": owner_updated_balance
                }
            )

            fields["buyer_id"] = buyer_id

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

#TODO: UPDATE BALANCE THROUGH BANK TRANSACTIONS
#TODO: CHANGE HTTP METHODS. SHOULD ONLY ACCEPT POST
@orders.route('/transaction', methods=['GET'])
def transaction():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'product_data': {
                            'name': 'test',
                        },
                        'unit_amount': 500,
                        'currency': 'usd',
                    },
                    'quantity': 1,
                },
            ],
            payment_method_types=['card'],
            mode='payment',
            success_url=request.host_url + 'orders/transaction/success',
            cancel_url=request.host_url + 'orders/transaction/cancel',
        )

    except Exception as e:
        log.exception(e)
        
    return redirect(checkout_session.url)

@orders.route('/transaction/success')
def success():
    return render_template('success.html')


@orders.route('/transaction/cancel')
def cancel():
    return render_template('../templates/cancel.html')