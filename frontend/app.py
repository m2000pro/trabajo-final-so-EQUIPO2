from flask import Flask
from routes import frontend_bp

app = Flask(__name__)

# Registramos las rutas
app.register_blueprint(frontend_bp)

if __name__ == '__main__':
    # Correrá en el puerto 5000 de tu Windows
    app.run(host='0.0.0.0', port=5000, debug=True)