"""
Pruebas básicas de humo: verifican que la app arranca y que las
rutas principales responden. Usan una base de datos SQLite en
memoria para no afectar la base de datos real.
"""

import pytest

from src.db.seed import poblar_ciclos, poblar_grados_y_materias
from src.main import crear_app
from src.model import db
from src.model.juego import Juego
from src.model.usuario import Usuario


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
        poblar_ciclos()
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


def test_nombre_de_la_escuela(client):
    respuesta = client.get("/")
    assert "Escuela León Cortés".encode() in respuesta.data
    assert b"Escuela Cot" not in respuesta.data


# ---------------------------- JUEGOS ----------------------------


def test_juegos_lista_los_tres_ciclos(client):
    respuesta = client.get("/juegos")
    assert respuesta.status_code == 200
    for nombre in (b"Preescolar", b"Primer Ciclo", b"Segundo Ciclo"):
        assert nombre in respuesta.data


def test_juegos_de_un_ciclo(client):
    assert client.get("/juegos/primer-ciclo").status_code == 200


def test_ciclo_inexistente_da_404(client):
    assert client.get("/juegos/no-existe").status_code == 404


def test_admin_juegos_requiere_login(client):
    assert client.get("/admin/juegos/1").status_code == 302


def _login(client, app):
    admin = Usuario(username="admin_test")
    admin.set_password("clave123")
    db.session.add(admin)
    db.session.commit()
    client.post("/admin/login", data={"username": "admin_test", "password": "clave123"})


def test_admin_agrega_oculta_y_elimina_juego(client, app):
    _login(client, app)

    r = client.post(
        "/admin/juegos/2",
        data={"titulo": "Memoria animal", "tipo": "enlace", "cuerpo": "https://ejemplo.com", "orden": "1"},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert Juego.query.count() == 1

    # Se ve en la página pública del ciclo, y NO en otro ciclo
    assert b"Memoria animal" in client.get("/juegos/primer-ciclo").data
    assert b"Memoria animal" not in client.get("/juegos/segundo-ciclo").data

    # Al ocultarlo, deja de verse
    juego = Juego.query.first()
    client.post(f"/admin/juegos/toggle/{juego.id}")
    assert b"Memoria animal" not in client.get("/juegos/primer-ciclo").data

    # Eliminar
    client.post(f"/admin/juegos/eliminar/{juego.id}")
    assert Juego.query.count() == 0


def test_juego_tipo_archivo_sin_archivo_da_error(client, app):
    _login(client, app)
    client.post("/admin/juegos/1", data={"titulo": "Sin archivo", "tipo": "archivo"})
    assert Juego.query.count() == 0


def test_juegos_no_aparecen_en_el_material_educativo(client, app):
    _login(client, app)
    client.post("/admin/juegos/1", data={"titulo": "Solo juego", "tipo": "texto", "cuerpo": "Hola"})
    assert b"Solo juego" not in client.get("/grado/preescolar-interactivo").data
