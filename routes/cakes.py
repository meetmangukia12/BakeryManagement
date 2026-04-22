from flask import Blueprint, request, jsonify
from db import db
from models import Cake, Customer

cakes_bp = Blueprint('cakes', __name__)

REQUIRED_FIELDS = ['Customer_id', 'Cake_shape', 'Cake_batter',
                   'Side_frosting', 'Top_frosting', 'Decoration_1', 'Layers']


def _validate_cake_data(data):
    """Returns an error string, or None if data is valid."""
    for field in REQUIRED_FIELDS:
        if data.get(field) in (None, ''):
            return f'{field} is required'
    layers = data.get('Layers')
    if layers is not None and not (1 <= int(layers) <= 5):
        return 'Layers must be between 1 and 5'
    return None


# GET /api/cakes — list all cakes (optional ?customer_id= filter)
@cakes_bp.route('/', methods=['GET'])
def get_all_cakes():
    query = Cake.query
    customer_id = request.args.get('customer_id', type=int)
    if customer_id:
        query = query.filter_by(Customer_id=customer_id)
    cakes = query.order_by(Cake.Cake_id).all()
    return jsonify([c.to_dict() for c in cakes]), 200


# GET /api/cakes/<id>
@cakes_bp.route('/<int:cake_id>', methods=['GET'])
def get_cake(cake_id):
    cake = Cake.query.get_or_404(cake_id, description='Cake not found')
    return jsonify(cake.to_dict()), 200


# POST /api/cakes — create a cake
@cakes_bp.route('/', methods=['POST'])
def create_cake():
    data = request.get_json()
    error = _validate_cake_data(data)
    if error:
        return jsonify({'error': error}), 400

    # Ensure the customer exists
    if not Customer.query.get(data['Customer_id']):
        return jsonify({'error': f"Customer {data['Customer_id']} not found"}), 404

    cake = Cake(
        Customer_id   = data['Customer_id'],
        Cake_shape    = data['Cake_shape'],
        Cake_batter   = data['Cake_batter'],
        Side_frosting = data['Side_frosting'],
        Top_frosting  = data['Top_frosting'],
        Decoration_1  = data['Decoration_1'],
        Decoration_2  = data.get('Decoration_2'),
        Layers        = int(data['Layers']),
    )
    db.session.add(cake)
    db.session.commit()
    return jsonify(cake.to_dict()), 201


# PUT /api/cakes/<id> — update a cake
@cakes_bp.route('/<int:cake_id>', methods=['PUT'])
def update_cake(cake_id):
    cake = Cake.query.get_or_404(cake_id, description='Cake not found')
    data = request.get_json()

    updatable = ['Cake_shape', 'Cake_batter', 'Side_frosting',
                 'Top_frosting', 'Decoration_1', 'Decoration_2']
    for field in updatable:
        if field in data:
            setattr(cake, field, data[field])

    if 'Layers' in data:
        layers = int(data['Layers'])
        if not (1 <= layers <= 5):
            return jsonify({'error': 'Layers must be between 1 and 5'}), 400
        cake.Layers = layers

    db.session.commit()
    return jsonify(cake.to_dict()), 200


# DELETE /api/cakes/<id>
@cakes_bp.route('/<int:cake_id>', methods=['DELETE'])
def delete_cake(cake_id):
    cake = Cake.query.get_or_404(cake_id, description='Cake not found')
    db.session.delete(cake)
    db.session.commit()
    return jsonify({'message': f'Cake {cake_id} deleted'}), 200
