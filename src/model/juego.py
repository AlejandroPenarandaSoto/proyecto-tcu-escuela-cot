"""
MODEL: Juego

Es el material de juegos que el administrador carga para un Ciclo
(Preescolar, Primer Ciclo o Segundo Ciclo). Funciona igual que el
material educativo (Contenido): cada juego es un bloque que puede ser
texto, video, imagen, archivo o enlace, ordenado por el campo `orden`.

Se guarda en una tabla aparte para que los juegos queden separados
del material educativo.
"""

from datetime import datetime

from src.model import db
from src.model.contenido import TipoContenido


class Juego(db.Model):
    __tablename__ = "juegos"

    id = db.Column(db.Integer, primary_key=True)

    ciclo_id = db.Column(db.Integer, db.ForeignKey("ciclos.id"), nullable=False)

    titulo = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default=TipoContenido.ENLACE)

    # Para TEXTO: el texto en sí. Para VIDEO/ENLACE: la URL.
    # Para IMAGEN/ARCHIVO: el nombre del archivo guardado en /static/uploads/
    cuerpo = db.Column(db.Text, nullable=True)

    orden = db.Column(db.Integer, nullable=False, default=0)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    ciclo = db.relationship("Ciclo", back_populates="juegos")

    def __repr__(self):
        return f"<Juego {self.titulo} (ciclo={self.ciclo_id})>"
