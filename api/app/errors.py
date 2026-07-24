from flask import jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from .extensions import db


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def manejar_error_http(error):
        return jsonify({
            "error": error.name,
            "mensaje": error.description,
            "codigo": error.code
        }), error.code

    @app.errorhandler(IntegrityError)
    def manejar_error_integridad(error):
        db.session.rollback()

        return jsonify({
            "error": "Conflicto de integridad",
            "mensaje": (
                "El registro enviado viola una "
                "restricción de la base de datos."
            ),
            "codigo": 409
        }), 409

    @app.errorhandler(Exception)
    def manejar_error_general(error):
        app.logger.exception(
            "Se produjo un error no controlado."
        )

        db.session.rollback()

        return jsonify({
            "error": "Error interno",
            "mensaje": (
                "Ocurrió un error inesperado "
                "en el servidor."
            ),
            "codigo": 500
        }), 500
