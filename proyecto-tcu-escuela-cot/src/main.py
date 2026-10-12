"""
Punto de entrada de la aplicación.

Usa el patrón "app factory": una función crea_app() que construye
y configura la instancia de Flask, registra el Modelo, la Vista
(templates/static) y el Controlador (Blueprints).

Ejecutar con:
    python -m src.main
"""

import os

from flask import Flask
from flask_login import LoginManager

from config import config_por_nombre
from src.model import db
from src.model.usuario import Usuario


def crear_app(nombre_config=None):
    nombre_config = nombre_config or os.environ.get("FLASK_ENV", "development")

    # template_folder y static_folder apuntan a la capa VISTA
    app = Flask(
        __name__,
        template_folder="vista/templates",
        static_folder="vista/static",
    )
    app.config.from_object(config_por_nombre[nombre_config])

    # --- Inicializar MODEL (SQLAlchemy) ---
    db.init_app(app)

    # --- Inicializar autenticación (solo para el módulo admin) ---
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Debes iniciar sesión para continuar."
    login_manager.login_message_category = "error"
    login_manager.init_app(app)

    @login_manager.user_loader
    def cargar_usuario(user_id):
        return Usuario.query.get(int(user_id))

    # --- Registrar CONTROLLER (Blueprints) ---
    from src.controller.admin_controller import admin_bp
    from src.controller.auth_controller import auth_bp
    from src.controller.estudiante_controller import estudiante_bp

    app.register_blueprint(estudiante_bp)
    app.register_blueprint(auth_bp, url_prefix="/admin")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app


if __name__ == "__main__":
    app = crear_app()
    app.run(debug=app.config.get("DEBUG", True))
