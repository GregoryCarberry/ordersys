from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .db import db
from .models.store import Store
from .config import Config
from .store_routes import store_routes




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
        from .models.store import Store

    # Register blueprints
    from .auth_routes import auth_bp
    from .admin_routes import admin_bp
    from .order_admin_routes import order_admin_routes
    from .warehouse_routes import warehouse_routes
    from .warehouse_product_routes import warehouse_products
    app.register_blueprint(warehouse_products)
    app.register_blueprint(warehouse_routes)
    app.register_blueprint(order_admin_routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(store_routes)

    return app
