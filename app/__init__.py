from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes.usuario_routes import usuario_bp
from app.routes.producto_routes import producto_bp
from app.routes.pedidos_routes import pedidos_bp
from app.routes.estadisticas_routes import estadisticas_bp
from app.utils.errors import register_error_handlers
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():

    app = Flask(__name__)

    JWTManager(app)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    app.register_blueprint(usuario_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(estadisticas_bp)

    register_error_handlers(app)

    return app