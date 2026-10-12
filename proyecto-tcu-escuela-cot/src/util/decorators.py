"""
UTIL: Decoradores.

flask_login.login_required ya cubre la protección básica de rutas.
Aquí se agregan decoradores adicionales específicos del proyecto,
como validar que el usuario esté activo.
"""

from functools import wraps

from flask import abort
from flask_login import current_user


def admin_activo_required(f):
    """
    Además de estar logueado, verifica que la cuenta del admin
    esté marcada como activa (por si se desea desactivar cuentas
    sin borrarlas).
    """

    @wraps(f)
    def decorador(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(
            current_user, "activo", False
        ):
            abort(403)
        return f(*args, **kwargs)

    return decorador
