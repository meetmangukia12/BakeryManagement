from flask import Blueprint, request, jsonify
from db import db
from sqlalchemy import text

views_bp = Blueprint('views', __name__)


def _rows_to_list(result):
    """Convert SQLAlchemy Row objects to a list of dicts."""
    keys = result.keys()
    return [dict(zip(keys, row)) for row in result]


# ------------------------------------------------------------------
# GET /api/views/order-details
# Full order summary (vw_Order_Details)
# Optional: ?customer_name=Alice+Johnson
# ------------------------------------------------------------------
@views_bp.route('/order-details', methods=['GET'])
def order_details():
    customer_name = request.args.get('customer_name')

    sql = "SELECT * FROM vw_Order_Details"
    params = {}
    if customer_name:
        sql += " WHERE Customer_name = :name"
        params['name'] = customer_name

    result = db.session.execute(text(sql), params)
    rows = _rows_to_list(result)

    # Serialize dates and decimals
    for row in rows:
        if row.get('Order_date'):
            row['Order_date'] = str(row['Order_date'])
        if row.get('Order_price') is not None:
            row['Order_price'] = float(row['Order_price'])

    return jsonify(rows), 200


# ------------------------------------------------------------------
# GET /api/views/invoice/<order_id>
# Customer-facing invoice (vw_Invoice)
# ------------------------------------------------------------------
@views_bp.route('/invoice/<int:order_id>', methods=['GET'])
def invoice(order_id):
    sql = "SELECT * FROM vw_Invoice WHERE Invoice_Number = :id"
    result = db.session.execute(text(sql), {'id': order_id})
    rows = _rows_to_list(result)

    if not rows:
        return jsonify({'error': f'Invoice for Order {order_id} not found'}), 404

    row = rows[0]
    if row.get('Order_date'):
        row['Order_date'] = str(row['Order_date'])
    if row.get('Amount_Due') is not None:
        row['Amount_Due'] = float(row['Amount_Due'])

    return jsonify(row), 200


# ------------------------------------------------------------------
# GET /api/views/production-schedule
# Upcoming production queue (vw_Production_Schedule)
# Optional: ?date=YYYY-MM-DD
# ------------------------------------------------------------------
@views_bp.route('/production-schedule', methods=['GET'])
def production_schedule():
    date_filter = request.args.get('date')

    sql = "SELECT * FROM vw_Production_Schedule"
    params = {}
    if date_filter:
        sql += " WHERE Order_date = :date"
        params['date'] = date_filter

    result = db.session.execute(text(sql), params)
    rows = _rows_to_list(result)

    for row in rows:
        if row.get('Order_date'):
            row['Order_date'] = str(row['Order_date'])

    return jsonify(rows), 200


# ------------------------------------------------------------------
# GET /api/views/revenue-summary
# Revenue by occasion & date (vw_Revenue_Summary)
# Optional: ?occasion=Birthday
# ------------------------------------------------------------------
@views_bp.route('/revenue-summary', methods=['GET'])
def revenue_summary():
    occasion = request.args.get('occasion')

    sql = "SELECT * FROM vw_Revenue_Summary"
    params = {}
    if occasion:
        sql += " WHERE Order_occasion = :occasion"
        params['occasion'] = occasion

    result = db.session.execute(text(sql), params)
    rows = _rows_to_list(result)

    for row in rows:
        if row.get('Order_date'):
            row['Order_date'] = str(row['Order_date'])
        for key in ('Daily_Revenue', 'Avg_Order_Price'):
            if row.get(key) is not None:
                row[key] = float(row[key])

    return jsonify(rows), 200


# ------------------------------------------------------------------
# GET /api/views/customer-history
# Customer lifetime value & order history (vw_Customer_Order_History)
# Optional: ?customer_name=Bob+Martinez
# ------------------------------------------------------------------
@views_bp.route('/customer-history', methods=['GET'])
def customer_history():
    customer_name = request.args.get('customer_name')

    sql = "SELECT * FROM vw_Customer_Order_History"
    params = {}
    if customer_name:
        sql += " WHERE Customer_name = :name"
        params['name'] = customer_name

    result = db.session.execute(text(sql), params)
    rows = _rows_to_list(result)

    for row in rows:
        if row.get('Last_Order_Date'):
            row['Last_Order_Date'] = str(row['Last_Order_Date'])
        if row.get('Lifetime_Spend') is not None:
            row['Lifetime_Spend'] = float(row['Lifetime_Spend'])

    return jsonify(rows), 200
