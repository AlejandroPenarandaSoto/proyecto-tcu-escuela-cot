"""
Configuración central de la aplicación.

Usamos SQLite como base de datos: es un solo archivo, gratuito,
sin necesidad de instalar un servidor de BD aparte. Ideal para este
proyecto, donde los estudiantes solo LEEN contenido y el admin
escribe ocasionalmente.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Clave secreta para sesiones (login del admin) y protección CSRF.
    # En producción, definir SECRET_KEY como variable de entorno real.
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")

    # Ruta del archivo de base de datos SQLite dentro de src/db/
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "src", "db", "escuela.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Carpeta donde se guardará el material que suba el administrador
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "src", "vista", "static", "uploads")
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB máximo por archivo subido


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_por_nombre = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
