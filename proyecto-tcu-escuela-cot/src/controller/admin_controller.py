"""
CONTROLLER: Módulo Administrador.

Rutas protegidas (requieren login). Permite editar el material
(Contenido) que ve cada grado en cada materia.
"""

import os
from datetime import datetime

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
from src.model.contenido import Contenido, TipoContenido
from src.model.grado import Grado
from src.model.materia import Materia
from src.util.decorators import admin_activo_required
from src.util.validators import extension_permitida

admin_bp = Blueprint("admin", __name__, template_folder="../vista/templates/admin")


@admin_bp.route("/dashboard")
@login_required
@admin_activo_required
def dashboard():
    grados = Grado.query.order_by(Grado.orden).all()
    materias = Materia.query.order_by(Materia.orden).all()
    return render_template("admin/dashboard.html", grados=grados, materias=materias)


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
        titulo = request.form.get("titulo", "").strip()
        tipo = request.form.get("tipo", TipoContenido.TEXTO)
        cuerpo_texto = request.form.get("cuerpo", "").strip()
        orden = request.form.get("orden", 0)
        archivo = request.files.get("archivo")

        cuerpo = cuerpo_texto

        # Si es imagen o archivo y se subió un archivo real, lo guardamos
        if tipo in ("imagen", "archivo") and archivo and archivo.filename:
            if not extension_permitida(archivo.filename, tipo):
                flash("Tipo de archivo no permitido.", "error")
                return redirect(
                    url_for(
                        "admin.editar_contenido",
                        grado_id=grado_id,
                        materia_id=materia_id,
                    )
                )

            nombre_seguro = secure_filename(archivo.filename)
            nombre_final = (
                f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{nombre_seguro}"
            )
            ruta_destino = os.path.join(
                current_app.config["UPLOAD_FOLDER"], nombre_final
            )
            os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
            archivo.save(ruta_destino)
            cuerpo = nombre_final

        nuevo = Contenido(
            grado_id=grado.id,
            materia_id=materia.id if materia else None,
            titulo=titulo,
            tipo=tipo,
            cuerpo=cuerpo,
            orden=int(orden) if str(orden).isdigit() else 0,
        )
        db.session.add(nuevo)
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
