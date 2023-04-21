from flask import Blueprint, jsonify, request

orders = Blueprint('orders', __name__)

@orders.route('/create', methods=['POST'])
def create():
    pass

@orders.route('/get', methods=['GET'])
def get():
    pass

@orders.route('/list', methods=['GET'])
def list():
    pass
