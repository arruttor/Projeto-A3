from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.produto_routes import produto_bp
    from app.routes.home_routes import home_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(home_bp)

    return app
