"""
CONTROLLER: Módulo Estudiante.

Rutas públicas, sin autenticación. El flujo es:
  1. GET /                -> el estudiante elige su grado
  2. GET /grado/<slug>    -> si el grado tiene materias, las elige;
                              si es preescolar, ve el contenido directo
  3. GET /grado/<slug>/materia/<slug> -> ve el contenido de esa materia
"""

from flask import Blueprint, abort, render_template

from src.model.contenido import Contenido
from src.model.grado import Grado
from src.model.materia import Materia

estudiante_bp = Blueprint(
    "estudiante", __name__, template_folder="../vista/templates/estudiante"
)


@estudiante_bp.route("/")
def seleccion_grado():
    grados = Grado.query.order_by(Grado.orden).all()
    return render_template("estudiante/seleccion_grado.html", grados=grados)


@estudiante_bp.route("/grado/<grado_slug>")
def ver_grado(grado_slug):
    grado = Grado.query.filter_by(slug=grado_slug).first_or_404()

    if grado.tiene_materias:
        materias = Materia.query.order_by(Materia.orden).all()
        return render_template(
            "estudiante/seleccion_materia.html", grado=grado, materias=materias
        )

    # Preescolar: no hay materias, se muestra el contenido directo del grado
    contenidos = (
        Contenido.query.filter_by(grado_id=grado.id, materia_id=None, activo=True)
        .order_by(Contenido.orden)
        .all()
    )
    return render_template(
        "estudiante/contenido.html",
        grado=grado,
        materia=None,
        contenidos=contenidos,
    )


@estudiante_bp.route("/grado/<grado_slug>/materia/<materia_slug>")
def ver_contenido(grado_slug, materia_slug):
    grado = Grado.query.filter_by(slug=grado_slug).first_or_404()
    materia = Materia.query.filter_by(slug=materia_slug).first_or_404()

    if not grado.tiene_materias:
        # Un preescolar no debería tener rutas de materia; evitar acceso inválido
        abort(404)

    contenidos = (
        Contenido.query.filter_by(
            grado_id=grado.id, materia_id=materia.id, activo=True
        )
        .order_by(Contenido.orden)
        .all()
    )
    return render_template(
        "estudiante/contenido.html",
        grado=grado,
        materia=materia,
        contenidos=contenidos,
    )
