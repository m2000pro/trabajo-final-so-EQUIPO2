from flask import Flask

from .config import Config
from .errors import register_error_handlers
from .extensions import db
from .routes import api_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    CORS(app)

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(api_bp)

    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app
