"""
CONTROLLER: Módulo Administrador.

Rutas protegidas (requieren login). Permite editar:
  - el material educativo (Contenido) de cada grado y materia, y
  - los juegos (Juego) de cada ciclo (Preescolar, Primer y Segundo Ciclo).
"""

import os
from datetime import datetime, timezone

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required
from werkzeug.utils import secure_filename

from src.model import db
from src.model.ciclo import Ciclo
from src.model.contenido import Contenido, TipoContenido
from src.model.grado import Grado
from src.model.juego import Juego
from src.model.materia import Materia
from src.util.decorators import admin_activo_required
from src.util.validators import extension_permitida

admin_bp = Blueprint("admin", __name__, template_folder="../vista/templates/admin")


def _leer_formulario_material():
    """
    Lee y valida el formulario de "Agregar contenido" / "Agregar juego".
    Es el mismo formulario para el material educativo y para los juegos.

    Si el tipo es imagen o archivo, guarda el archivo subido en UPLOAD_FOLDER.

    Devuelve (datos, error): si hay un problema, datos es None y error
    trae el mensaje para mostrarle al administrador.
    """
    titulo = request.form.get("titulo", "").strip()
    tipo = request.form.get("tipo", TipoContenido.TEXTO)
    orden = request.form.get("orden", 0)
    cuerpo = request.form.get("cuerpo", "").strip()

    if not titulo:
        return None, "El título es obligatorio."
    if tipo not in TipoContenido.OPCIONES:
        return None, "Tipo de contenido no válido."

    # Si es imagen o archivo, hay que subir un archivo real
    if tipo in (TipoContenido.IMAGEN, TipoContenido.ARCHIVO):
        archivo = request.files.get("archivo")
        if not archivo or not archivo.filename:
            return None, "Debes seleccionar un archivo para subir."
        if not extension_permitida(archivo.filename, tipo):
            return None, "Tipo de archivo no permitido."

        nombre_seguro = secure_filename(archivo.filename)
        marca_tiempo = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        nombre_final = f"{marca_tiempo}_{nombre_seguro}"
        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
        archivo.save(os.path.join(current_app.config["UPLOAD_FOLDER"], nombre_final))
        cuerpo = nombre_final

    datos = {
        "titulo": titulo,
        "tipo": tipo,
        "cuerpo": cuerpo,
        "orden": int(orden) if str(orden).isdigit() else 0,
    }
    return datos, None


@admin_bp.route("/dashboard")
@login_required
@admin_activo_required
def dashboard():
    grados = Grado.query.order_by(Grado.orden).all()
    materias = Materia.query.order_by(Materia.orden).all()
    ciclos = Ciclo.query.order_by(Ciclo.orden).all()
    return render_template(
        "admin/dashboard.html", grados=grados, materias=materias, ciclos=ciclos
    )


@admin_bp.route(
    "/contenido/<int:grado_id>", defaults={"materia_id": None}, methods=["GET", "POST"]
)
@admin_bp.route("/contenido/<int:grado_id>/<int:materia_id>", methods=["GET", "POST"])
@login_required
@admin_activo_required
def editar_contenido(grado_id, materia_id):
    grado = Grado.query.get_or_404(grado_id)
    materia = Materia.query.get_or_404(materia_id) if materia_id else None

    # Validación: si el grado no tiene materias, materia_id debe ser None y viceversa
    if grado.tiene_materias and materia is None:
        flash("Este grado requiere seleccionar una materia.", "error")
        return redirect(url_for("admin.dashboard"))
    if not grado.tiene_materias and materia is not None:
        flash("Este grado (preescolar) no maneja materias.", "error")
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        datos, error = _leer_formulario_material()
        if error:
            flash(error, "error")
        else:
            db.session.add(
                Contenido(
                    grado_id=grado.id,
                    materia_id=materia.id if materia else None,
                    **datos,
                )
            )
            db.session.commit()
            flash("Contenido agregado correctamente.", "success")
        return redirect(
            url_for(
                "admin.editar_contenido", grado_id=grado_id, materia_id=materia_id
            )
        )

    contenidos = (
        Contenido.query.filter_by(grado_id=grado.id, materia_id=materia_id)
        .order_by(Contenido.orden)
        .all()
    )
    return render_template(
        "admin/editar_contenido.html",
        grado=grado,
        materia=materia,
        contenidos=contenidos,
        tipos=TipoContenido.OPCIONES,
    )


@admin_bp.route("/contenido/eliminar/<int:contenido_id>", methods=["POST"])
@login_required
@admin_activo_required
def eliminar_contenido(contenido_id):
    contenido = Contenido.query.get_or_404(contenido_id)
    grado_id = contenido.grado_id
    materia_id = contenido.materia_id

    db.session.delete(contenido)
    db.session.commit()
    flash("Contenido eliminado.", "success")
    return redirect(
        url_for("admin.editar_contenido", grado_id=grado_id, materia_id=materia_id)
    )


@admin_bp.route("/contenido/toggle/<int:contenido_id>", methods=["POST"])
@login_required
@admin_activo_required
def toggle_contenido(contenido_id):
    """Activa/desactiva un contenido sin borrarlo (ej. para ocultarlo temporalmente)."""
    contenido = Contenido.query.get_or_404(contenido_id)
    contenido.activo = not contenido.activo
    db.session.commit()
    return redirect(
        url_for(
            "admin.editar_contenido",
            grado_id=contenido.grado_id,
            materia_id=contenido.materia_id,
        )
    )


# =====================================================================
# JUEGOS (organizados por ciclo, no por grado)
# =====================================================================


@admin_bp.route("/juegos/<int:ciclo_id>", methods=["GET", "POST"])
@login_required
@admin_activo_required
def editar_juegos(ciclo_id):
    ciclo = Ciclo.query.get_or_404(ciclo_id)

    if request.method == "POST":
        datos, error = _leer_formulario_material()
        if error:
            flash(error, "error")
        else:
            db.session.add(Juego(ciclo_id=ciclo.id, **datos))
            db.session.commit()
            flash("Juego agregado correctamente.", "success")
        return redirect(url_for("admin.editar_juegos", ciclo_id=ciclo_id))

    juegos = Juego.query.filter_by(ciclo_id=ciclo.id).order_by(Juego.orden).all()
    return render_template(
        "admin/editar_juegos.html",
        ciclo=ciclo,
        juegos=juegos,
        tipos=TipoContenido.OPCIONES,
    )


@admin_bp.route("/juegos/eliminar/<int:juego_id>", methods=["POST"])
@login_required
@admin_activo_required
def eliminar_juego(juego_id):
    juego = Juego.query.get_or_404(juego_id)
    ciclo_id = juego.ciclo_id

    db.session.delete(juego)
    db.session.commit()
    flash("Juego eliminado.", "success")
    return redirect(url_for("admin.editar_juegos", ciclo_id=ciclo_id))


@admin_bp.route("/juegos/toggle/<int:juego_id>", methods=["POST"])
@login_required
@admin_activo_required
def toggle_juego(juego_id):
    """Activa/desactiva un juego sin borrarlo (ej. para ocultarlo temporalmente)."""
    juego = Juego.query.get_or_404(juego_id)
    juego.activo = not juego.activo
    db.session.commit()
    return redirect(url_for("admin.editar_juegos", ciclo_id=juego.ciclo_id))
