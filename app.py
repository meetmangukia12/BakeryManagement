from flask import Flask
from config import Config
from db import db
from routes.customers import customers_bp
from routes.cakes import cakes_bp
from routes.orders import orders_bp
from routes.views import views_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(cakes_bp,     url_prefix='/api/cakes')
    app.register_blueprint(orders_bp,    url_prefix='/api/orders')
    app.register_blueprint(views_bp,     url_prefix='/api/views')

    @app.route('/')
    def index():
        return {
            "message": "Bakery Management API",
            "version": "1.0",
            "endpoints": {
                "customers": "/api/customers",
                "cakes":     "/api/cakes",
                "orders":    "/api/orders",
                "views":     "/api/views"
            }
        }

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
