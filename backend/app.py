# app.py
from flask import Flask
from flask_cors import CORS
from routes import cargo_bp, login_bp, evento_bp

app = Flask(__name__)


CORS(app, resources={r"/api/*": {"origins": [
    "http://localhost:5173",
    "http://probable-guide-rpv9wgwp5j5fpgvw-5173.app.github.dev"
]}})

# Registrando as rotas
app.register_blueprint(cargo_bp, url_prefix="/api")
app.register_blueprint(login_bp, url_prefix="/api")
app.register_blueprint(evento_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

