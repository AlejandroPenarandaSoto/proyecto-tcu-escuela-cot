"""
MODEL: Grado

Representa cada nivel escolar que un estudiante puede elegir:
Preescolar Interactivo, Preescolar Transición, Primero, Segundo,
Tercero, Cuarto, Quinto y Sexto.

Los preescolares NO tienen materias (van directo a su contenido).
Primero a Sexto SÍ tienen materias asociadas.
"""

from src.model import db


class Grado(db.Model):
    __tablename__ = "grados"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)  # usado en la URL
    orden = db.Column(db.Integer, nullable=False, default=0)  # orden de despliegue
    tiene_materias = db.Column(db.Boolean, nullable=False, default=True)

    # Relación con el contenido asociado a este grado
    contenidos = db.relationship(
        "Contenido", back_populates="grado", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Grado {self.nombre}>"
