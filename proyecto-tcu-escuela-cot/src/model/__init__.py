"""
Paquete MODEL.

Aquí vive la instancia única de SQLAlchemy (db) que usan todas las
entidades del modelo, y que se inicializa en src/main.py con la app
de Flask (patrón app factory).
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
