"""
MODEL: Materia

Representa cada materia disponible para los grados de Primero a Sexto:
Ciencias, Matemática, Español, Estudios Sociales, Inglés, Religión,
Educación Musical y Educación Física.
"""

from src.model import db


class Materia(db.Model):
    __tablename__ = "materias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    orden = db.Column(db.Integer, nullable=False, default=0)
    icono = db.Column(db.String(50), nullable=True)  # ej: nombre de un ícono/emoji

    contenidos = db.relationship(
        "Contenido", back_populates="materia", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Materia {self.nombre}>"
