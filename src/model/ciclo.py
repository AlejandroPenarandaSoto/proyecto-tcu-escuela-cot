"""
MODEL: Ciclo

Los juegos NO se organizan por grado sino por ciclo escolar:
Preescolar, Primer Ciclo (1° a 3°) y Segundo Ciclo (4° a 6°).
"""

from src.model import db


class Ciclo(db.Model):
    __tablename__ = "ciclos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)  # usado en la URL
    descripcion = db.Column(db.String(120), nullable=True)  # ej: "1° a 3° grado"
    orden = db.Column(db.Integer, nullable=False, default=0)

    juegos = db.relationship(
        "Juego", back_populates="ciclo", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Ciclo {self.nombre}>"
