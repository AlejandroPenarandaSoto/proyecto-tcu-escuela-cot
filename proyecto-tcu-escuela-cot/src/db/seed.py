"""
DB: Seed inicial.

Crea todas las tablas (si no existen) y carga los datos fijos de
Grados y Materias, que no dependen del administrador: son parte
de la estructura curricular de la escuela.

Uso:
    python -m src.db.seed
"""

from src.main import crear_app
from src.model import db
from src.model.grado import Grado
from src.model.materia import Materia

GRADOS = [
    # (nombre, slug, tiene_materias, orden)
    ("Preescolar Interactivo", "preescolar-interactivo", False, 1),
    ("Preescolar Transición", "preescolar-transicion", False, 2),
    ("Primero", "primero", True, 3),
    ("Segundo", "segundo", True, 4),
    ("Tercero", "tercero", True, 5),
    ("Cuarto", "cuarto", True, 6),
    ("Quinto", "quinto", True, 7),
    ("Sexto", "sexto", True, 8),
]

MATERIAS = [
    # (nombre, slug, orden)
    ("Ciencias", "ciencias", 1),
    ("Matemática", "matematica", 2),
    ("Español", "espanol", 3),
    ("Estudios Sociales", "estudios-sociales", 4),
    ("Inglés", "ingles", 5),
    ("Religión", "religion", 6),
    ("Educación Musical", "educacion-musical", 7),
    ("Educación Física", "educacion-fisica", 8),
]


def poblar_grados_y_materias():
    for nombre, slug, tiene_materias, orden in GRADOS:
        if not Grado.query.filter_by(slug=slug).first():
            db.session.add(
                Grado(
                    nombre=nombre,
                    slug=slug,
                    tiene_materias=tiene_materias,
                    orden=orden,
                )
            )

    for nombre, slug, orden in MATERIAS:
        if not Materia.query.filter_by(slug=slug).first():
            db.session.add(Materia(nombre=nombre, slug=slug, orden=orden))

    db.session.commit()
    print("Grados y materias cargados correctamente.")


if __name__ == "__main__":
    app = crear_app()
    with app.app_context():
        db.create_all()
        poblar_grados_y_materias()
