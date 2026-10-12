"""
CONTROLLER: Autenticación del administrador.

Único módulo con usuario/contraseña. Los estudiantes nunca pasan
por aquí.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from src.model.usuario import Usuario

auth_bp = Blueprint("auth", __name__, template_folder="../vista/templates/admin")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and usuario.activo and usuario.check_password(password):
            login_user(usuario)
            return redirect(url_for("admin.dashboard"))

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("admin/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))
