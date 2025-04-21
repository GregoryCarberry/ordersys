from flask import Flask
from flask_cors import CORS
from flask_session import Session
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
    Session(app)

    # Register blueprints
    from app.auth_routes import auth_bp
    from app.admin_routes import admin_bp  
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)        

    return app
