from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from db import db
from flasgger import Swagger
import os

# Routes
from routes.auth_routes import auth_bp
from routes.vegetable_routes import vegetable_bp
from models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    JWTManager(app)

    # Swagger config
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Vegetable Shop API",
            "description": "API for managing vegetables with JWT authentication",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT token: Bearer {your_token}"
            }
        },
        "security": [{"Bearer": []}]
    })

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(vegetable_bp, url_prefix="/vegetables")

    # DB setup
    with app.app_context():
        db.create_all()
        seed_admin()
        add_vegetable("Carrot", 0.5, 100)
        add_vegetable("Broccoli", 1.0, 50)
        add_vegetable("Spinach", 0.8, 75)

    return app

def seed_admin():
    """Create default admin user if not exists"""
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin")
        admin.set_password(os.getenv("ADMIN_PASSWORD", "password123"))  # hashed automatically
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created with username=admin, password=password123")

def add_vegetable(name, price, stock):
    """Add a vegetable if it doesn't exist"""
    from models.vegetable import Vegetable
    if not Vegetable.query.filter_by(name=name).first():
        veg = Vegetable(name=name, price=price, stock=stock)
        db.session.add(veg)
        db.session.commit()
        print(f"✅ Vegetable added: {name}")

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
