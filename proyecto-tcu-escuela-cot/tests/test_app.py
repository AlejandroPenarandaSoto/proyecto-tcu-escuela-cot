"""
Pruebas básicas de humo: verifican que la app arranca y que las
rutas principales responden. Usan una base de datos SQLite en
memoria para no afectar la base de datos real.
"""

import pytest

from src.db.seed import poblar_grados_y_materias
from src.main import crear_app
from src.model import db


@pytest.fixture
def app():
    app = crear_app("development")
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    )
    with app.app_context():
        db.create_all()
        poblar_grados_y_materias()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_pagina_inicio_lista_grados(client):
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert "grado".encode() in respuesta.data.lower() or b"Preescolar" in respuesta.data


def test_grado_con_materias_muestra_seleccion_materia(client):
    respuesta = client.get("/grado/primero")
    assert respuesta.status_code == 200
    assert b"Matem" in respuesta.data  # "Matem\xc3\xa1tica"


def test_grado_preescolar_no_pide_materia(client):
    respuesta = client.get("/grado/preescolar-interactivo")
    assert respuesta.status_code == 200


def test_grado_inexistente_da_404(client):
    respuesta = client.get("/grado/no-existe")
    assert respuesta.status_code == 404


def test_admin_dashboard_requiere_login(client):
    respuesta = client.get("/admin/dashboard")
    # Debe redirigir al login (302) porque no hay sesión iniciada
    assert respuesta.status_code == 302
