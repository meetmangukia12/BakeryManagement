# Bakery Management API

A Flask REST API backend for the Bakery Management System database.

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure your database connection
Edit `config.py` **or** set the `DATABASE_URL` environment variable:
```bash
export DATABASE_URL="mysql+pymysql://root:yourpassword@localhost:3306/BakeryManagementDB"
```

> Make sure you have already run the SQL script to create and populate the database.

### 3. Run the server
```bash
python app.py
```
The API will be available at `http://localhost:5000`.

---

## Project Structure

```
bakery_api/
├── app.py              # App factory & entry point
├── config.py           # DB URI and Flask config
├── db.py               # SQLAlchemy instance
├── requirements.txt
├── models/
│   └── __init__.py     # Customer, Cake, Order models
└── routes/
    ├── customers.py    # /api/customers
    ├── cakes.py        # /api/cakes
    ├── orders.py       # /api/orders
    └── views.py        # /api/views  (mirrors SQL views)
```

---

## API Reference

### Customers  `/api/customers`

| Method | URL                        | Description              |
|--------|----------------------------|--------------------------|
| GET    | `/api/customers/`          | List all customers        |
| GET    | `/api/customers/<id>`      | Get a single customer     |
| POST   | `/api/customers/`          | Create a customer         |
| PUT    | `/api/customers/<id>`      | Update a customer         |
| DELETE | `/api/customers/<id>`      | Delete (cascades to cakes)|

**POST / PUT body fields:**
```json
{
  "Customer_name":  "Alice Johnson",   // required on POST
  "Customer_age":   30,
  "Customer_email": "alice@email.com",
  "Customer_phone": "201-555-0101"
}
```

---

### Cakes  `/api/cakes`

| Method | URL                  | Description                           |
|--------|----------------------|---------------------------------------|
| GET    | `/api/cakes/`        | List all cakes (`?customer_id=1`)     |
| GET    | `/api/cakes/<id>`    | Get a single cake                     |
| POST   | `/api/cakes/`        | Create a cake                         |
| PUT    | `/api/cakes/<id>`    | Update a cake                         |
| DELETE | `/api/cakes/<id>`    | Delete a cake (cascades to orders)    |

**POST body fields:**
```json
{
  "Customer_id":   1,
  "Cake_shape":    "Round",
  "Cake_batter":   "Vanilla",
  "Side_frosting": "Buttercream",
  "Top_frosting":  "Whipped Cream",
  "Decoration_1":  "Fresh Flowers",
  "Decoration_2":  "Gold Leaf",       // optional
  "Layers":        2
}
```

---

### Orders  `/api/orders`

| Method | URL                   | Description                                         |
|--------|-----------------------|-----------------------------------------------------|
| GET    | `/api/orders/`        | List all orders                                     |
| GET    | `/api/orders/`        | Filter: `?occasion=Birthday`                        |
| GET    | `/api/orders/`        | Filter: `?start=2025-04-10&end=2025-04-18`          |
| GET    | `/api/orders/<id>`    | Get a single order                                  |
| POST   | `/api/orders/`        | Place a new order                                   |
| PUT    | `/api/orders/<id>`    | Update an order                                     |
| DELETE | `/api/orders/<id>`    | Cancel/delete an order                              |

**POST body fields:**
```json
{
  "Cake_id":          1,
  "Order_occasion":   "Birthday",      // optional
  "Shipping_address": "12 Oak St, NJ",
  "Order_price":      85.00,
  "Order_date":       "2025-05-01"
}
```

---

### Views  `/api/views`

These endpoints map directly to the SQL views in your database.

| Method | URL                                            | SQL View                    | Filter Param         |
|--------|------------------------------------------------|-----------------------------|----------------------|
| GET    | `/api/views/order-details`                    | `vw_Order_Details`          | `?customer_name=`    |
| GET    | `/api/views/invoice/<order_id>`               | `vw_Invoice`                | —                    |
| GET    | `/api/views/production-schedule`              | `vw_Production_Schedule`    | `?date=YYYY-MM-DD`   |
| GET    | `/api/views/revenue-summary`                  | `vw_Revenue_Summary`        | `?occasion=`         |
| GET    | `/api/views/customer-history`                 | `vw_Customer_Order_History` | `?customer_name=`    |

---

## Example Requests

```bash
# Get all birthday orders
curl "http://localhost:5000/api/orders/?occasion=Birthday"

# Get production schedule for April 12
curl "http://localhost:5000/api/views/production-schedule?date=2025-04-12"

# Get invoice for order #2
curl "http://localhost:5000/api/views/invoice/2"

# Create a new customer
curl -X POST http://localhost:5000/api/customers/ \
  -H "Content-Type: application/json" \
  -d '{"Customer_name": "Jane Doe", "Customer_age": 29, "Customer_email": "jane@email.com"}'

# Update a cake frosting (last-minute change)
curl -X PUT http://localhost:5000/api/cakes/1 \
  -H "Content-Type: application/json" \
  -d '{"Side_frosting": "Swiss Meringue"}'

# Cancel an order
curl -X DELETE http://localhost:5000/api/orders/7
```
