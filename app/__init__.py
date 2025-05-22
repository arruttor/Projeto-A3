from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)


    from app.routes.auth_routes import auth_bp
    from app.routes.produto_routes import main_bp



    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)


    return app