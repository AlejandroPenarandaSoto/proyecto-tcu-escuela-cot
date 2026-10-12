"""
DB: Utilidad para crear un usuario administrador desde la terminal.

Uso:
    python -m src.db.crear_admin
"""

import getpass

from src.main import crear_app
from src.model import db
from src.model.usuario import Usuario


def crear_admin():
    username = input("Usuario para el administrador: ").strip()
    nombre_completo = input("Nombre completo (opcional): ").strip()
    password = getpass.getpass("Contraseña: ")
    password_confirm = getpass.getpass("Confirmar contraseña: ")

    if password != password_confirm:
        print("Las contraseñas no coinciden. Intenta de nuevo.")
        return

    if Usuario.query.filter_by(username=username).first():
        print(f'Ya existe un usuario con el nombre "{username}".')
        return

    admin = Usuario(username=username, nombre_completo=nombre_completo or None)
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()
    print(f'Administrador "{username}" creado correctamente.')


if __name__ == "__main__":
    app = crear_app()
    with app.app_context():
        crear_admin()
