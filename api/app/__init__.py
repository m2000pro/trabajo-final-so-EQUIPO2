from flask import Flask

from .config import Config
from .errors import register_error_handlers
from .extensions import db
from .routes import api_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(api_bp)

    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app
