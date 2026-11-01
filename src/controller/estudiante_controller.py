"""
CONTROLLER: Módulo Estudiante.

Rutas públicas, sin autenticación. El flujo es:
  1. GET /                -> el estudiante elige su grado
  2. GET /grado/<slug>    -> si el grado tiene materias, las elige;
                              si es preescolar, ve el contenido directo
  3. GET /grado/<slug>/materia/<slug> -> ve el contenido de esa materia

Juegos (sección aparte, organizada por ciclo y no por grado):
  4. GET /juegos              -> el estudiante elige su ciclo
  5. GET /juegos/<ciclo_slug> -> ve los juegos de ese ciclo
"""

from flask import Blueprint, abort, render_template

from src.model.ciclo import Ciclo
from src.model.contenido import Contenido
from src.model.grado import Grado
from src.model.juego import Juego
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


@estudiante_bp.route("/juegos")
def seleccion_ciclo():
    ciclos = Ciclo.query.order_by(Ciclo.orden).all()
    return render_template("estudiante/seleccion_ciclo.html", ciclos=ciclos)


@estudiante_bp.route("/juegos/<ciclo_slug>")
def ver_juegos(ciclo_slug):
    ciclo = Ciclo.query.filter_by(slug=ciclo_slug).first_or_404()
    juegos = (
        Juego.query.filter_by(ciclo_id=ciclo.id, activo=True)
        .order_by(Juego.orden)
        .all()
    )
    return render_template("estudiante/juegos.html", ciclo=ciclo, juegos=juegos)
