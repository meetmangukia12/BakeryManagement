from db import db
from sqlalchemy import CheckConstraint


class Customer(db.Model):
    __tablename__ = 'Customer'

    Customer_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_name  = db.Column(db.String(100), nullable=False)
    Customer_age   = db.Column(db.Integer)
    Customer_email = db.Column(db.String(150))
    Customer_phone = db.Column(db.String(20))

    __table_args__ = (
        CheckConstraint('Customer_age >= 0', name='chk_customer_age'),
    )

    cakes = db.relationship('Cake', back_populates='customer', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'Customer_id':    self.Customer_id,
            'Customer_name':  self.Customer_name,
            'Customer_age':   self.Customer_age,
            'Customer_email': self.Customer_email,
            'Customer_phone': self.Customer_phone,
        }


class Cake(db.Model):
    __tablename__ = 'Cake'

    Cake_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_id   = db.Column(db.Integer, db.ForeignKey('Customer.Customer_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Cake_shape    = db.Column(db.String(50),  nullable=False)
    Cake_batter   = db.Column(db.String(50),  nullable=False)
    Side_frosting = db.Column(db.String(50),  nullable=False)
    Top_frosting  = db.Column(db.String(50),  nullable=False)
    Decoration_1  = db.Column(db.String(100), nullable=False)
    Decoration_2  = db.Column(db.String(100))
    Layers        = db.Column(db.Integer,     nullable=False)

    __table_args__ = (
        CheckConstraint('Layers BETWEEN 1 AND 5', name='chk_layers'),
    )

    customer = db.relationship('Customer', back_populates='cakes')
    orders   = db.relationship('Order', back_populates='cake', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'Cake_id':       self.Cake_id,
            'Customer_id':   self.Customer_id,
            'Cake_shape':    self.Cake_shape,
            'Cake_batter':   self.Cake_batter,
            'Side_frosting': self.Side_frosting,
            'Top_frosting':  self.Top_frosting,
            'Decoration_1':  self.Decoration_1,
            'Decoration_2':  self.Decoration_2,
            'Layers':        self.Layers,
        }


class Order(db.Model):
    __tablename__ = 'Order'

    Order_id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Cake_id          = db.Column(db.Integer, db.ForeignKey('Cake.Cake_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Order_occasion   = db.Column(db.String(100))
    Shipping_address = db.Column(db.String(255), nullable=False)
    Order_price      = db.Column(db.Numeric(10, 2), nullable=False)
    Order_date       = db.Column(db.Date, nullable=False)

    cake = db.relationship('Cake', back_populates='orders')

    def to_dict(self):
        return {
            'Order_id':         self.Order_id,
            'Cake_id':          self.Cake_id,
            'Order_occasion':   self.Order_occasion,
            'Shipping_address': self.Shipping_address,
            'Order_price':      float(self.Order_price),
            'Order_date':       self.Order_date.isoformat() if self.Order_date else None,
        }
