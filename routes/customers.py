from flask import Blueprint, request, jsonify
from db import db
from models import Customer

customers_bp = Blueprint('customers', __name__)


# GET /api/customers — list all customers
@customers_bp.route('/', methods=['GET'])
def get_all_customers():
    customers = Customer.query.order_by(Customer.Customer_id).all()
    return jsonify([c.to_dict() for c in customers]), 200


# GET /api/customers/<id> — get a single customer
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id, description='Customer not found')
    return jsonify(customer.to_dict()), 200


# POST /api/customers — create a new customer
@customers_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()

    required = ['Customer_name']
    for field in required:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400

    age = data.get('Customer_age')
    if age is not None and age < 0:
        return jsonify({'error': 'Customer_age must be >= 0'}), 400

    customer = Customer(
        Customer_name  = data['Customer_name'],
        Customer_age   = age,
        Customer_email = data.get('Customer_email'),
        Customer_phone = data.get('Customer_phone'),
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201


# PUT /api/customers/<id> — update a customer
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id, description='Customer not found')
    data = request.get_json()

    if 'Customer_name' in data:
        if not data['Customer_name']:
            return jsonify({'error': 'Customer_name cannot be empty'}), 400
        customer.Customer_name = data['Customer_name']

    if 'Customer_age' in data:
        if data['Customer_age'] is not None and data['Customer_age'] < 0:
            return jsonify({'error': 'Customer_age must be >= 0'}), 400
        customer.Customer_age = data['Customer_age']

    if 'Customer_email' in data:
        customer.Customer_email = data['Customer_email']

    if 'Customer_phone' in data:
        customer.Customer_phone = data['Customer_phone']

    db.session.commit()
    return jsonify(customer.to_dict()), 200


# DELETE /api/customers/<id> — delete a customer (cascades to cakes & orders)
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id, description='Customer not found')
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': f'Customer {customer_id} deleted'}), 200
