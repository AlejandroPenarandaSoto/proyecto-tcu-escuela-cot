"""
MODEL: Contenido

Es el material educativo que el administrador carga para una
combinación Grado + Materia (o solo Grado, en el caso de preescolar).

Un "bloque de contenido" puede ser texto, un enlace a video, una
imagen o un archivo (PDF, etc.). Cada grado-materia puede tener
varios bloques, ordenados por el campo `orden`.
"""

from datetime import datetime

from src.model import db


class TipoContenido:
    TEXTO = "texto"
    VIDEO = "video"
    IMAGEN = "imagen"
    ARCHIVO = "archivo"
    ENLACE = "enlace"

    OPCIONES = [TEXTO, VIDEO, IMAGEN, ARCHIVO, ENLACE]


class Contenido(db.Model):
    __tablename__ = "contenidos"

    id = db.Column(db.Integer, primary_key=True)

    grado_id = db.Column(db.Integer, db.ForeignKey("grados.id"), nullable=False)
    # materia_id es NULL cuando el grado es preescolar (no tiene materias)
    materia_id = db.Column(db.Integer, db.ForeignKey("materias.id"), nullable=True)

    titulo = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default=TipoContenido.TEXTO)

    # Para TEXTO: el texto en sí. Para VIDEO/ENLACE: la URL.
    # Para IMAGEN/ARCHIVO: el nombre del archivo guardado en /static/uploads/
    cuerpo = db.Column(db.Text, nullable=True)

    orden = db.Column(db.Integer, nullable=False, default=0)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    grado = db.relationship("Grado", back_populates="contenidos")
    materia = db.relationship("Materia", back_populates="contenidos")

    def __repr__(self):
        return f"<Contenido {self.titulo} (grado={self.grado_id}, materia={self.materia_id})>"
