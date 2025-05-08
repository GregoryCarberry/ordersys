from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from app.db import db
from app.models.store import Store
from app.config import Config
from app.store_routes import store_routes




migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
    Session(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # defer importing models until app is set up
    with app.app_context():
        from app.models.store import Store

    # Register blueprints
    from app.auth_routes import auth_bp
    from app.admin_routes import admin_bp
    from app.order_admin_routes import order_admin_routes
    from app.warehouse_routes import warehouse_routes
    from app.warehouse_product_routes import warehouse_products
    app.register_blueprint(warehouse_products)
    app.register_blueprint(warehouse_routes)
    app.register_blueprint(order_admin_routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(store_routes)

    return app
