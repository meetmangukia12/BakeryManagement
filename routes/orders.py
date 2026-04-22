from flask import Blueprint, request, jsonify
from db import db
from models import Order, Cake
from datetime import date

orders_bp = Blueprint('orders', __name__)


def _parse_date(date_str):
    try:
        return date.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None


# GET /api/orders
# Optional query params: ?occasion=Birthday  ?start=YYYY-MM-DD  ?end=YYYY-MM-DD
@orders_bp.route('/', methods=['GET'])
def get_all_orders():
    query = Order.query

    occasion = request.args.get('occasion')
    if occasion:
        query = query.filter(Order.Order_occasion == occasion)

    start = request.args.get('start')
    end   = request.args.get('end')
    if start:
        start_date = _parse_date(start)
        if not start_date:
            return jsonify({'error': 'Invalid start date. Use YYYY-MM-DD'}), 400
        query = query.filter(Order.Order_date >= start_date)
    if end:
        end_date = _parse_date(end)
        if not end_date:
            return jsonify({'error': 'Invalid end date. Use YYYY-MM-DD'}), 400
        query = query.filter(Order.Order_date <= end_date)

    orders = query.order_by(Order.Order_date).all()
    return jsonify([o.to_dict() for o in orders]), 200


# GET /api/orders/<id>
@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id, description='Order not found')
    return jsonify(order.to_dict()), 200


# POST /api/orders — place a new order
@orders_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()

    required = ['Cake_id', 'Shipping_address', 'Order_price', 'Order_date']
    for field in required:
        if data.get(field) in (None, ''):
            return jsonify({'error': f'{field} is required'}), 400

    if not Cake.query.get(data['Cake_id']):
        return jsonify({'error': f"Cake {data['Cake_id']} not found"}), 404

    order_date = _parse_date(data['Order_date'])
    if not order_date:
        return jsonify({'error': 'Invalid Order_date. Use YYYY-MM-DD'}), 400

    try:
        price = float(data['Order_price'])
        if price < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': 'Order_price must be a positive number'}), 400

    order = Order(
        Cake_id          = data['Cake_id'],
        Order_occasion   = data.get('Order_occasion'),
        Shipping_address = data['Shipping_address'],
        Order_price      = price,
        Order_date       = order_date,
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201


# PUT /api/orders/<id> — update an order
@orders_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id, description='Order not found')
    data  = request.get_json()

    if 'Order_occasion' in data:
        order.Order_occasion = data['Order_occasion']

    if 'Shipping_address' in data:
        if not data['Shipping_address']:
            return jsonify({'error': 'Shipping_address cannot be empty'}), 400
        order.Shipping_address = data['Shipping_address']

    if 'Order_price' in data:
        try:
            price = float(data['Order_price'])
            if price < 0:
                raise ValueError
            order.Order_price = price
        except (ValueError, TypeError):
            return jsonify({'error': 'Order_price must be a positive number'}), 400

    if 'Order_date' in data:
        order_date = _parse_date(data['Order_date'])
        if not order_date:
            return jsonify({'error': 'Invalid Order_date. Use YYYY-MM-DD'}), 400
        order.Order_date = order_date

    db.session.commit()
    return jsonify(order.to_dict()), 200


# DELETE /api/orders/<id> — cancel an order
@orders_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id, description='Order not found')
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': f'Order {order_id} cancelled and deleted'}), 200
