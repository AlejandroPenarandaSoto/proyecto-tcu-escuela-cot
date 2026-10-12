"""
UTIL: Validaciones reutilizables.
"""

EXTENSIONES_PERMITIDAS = {
    "imagen": {"png", "jpg", "jpeg", "gif", "webp"},
    "archivo": {"pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx"},
}


def extension_permitida(nombre_archivo: str, tipo: str) -> bool:
    """
    Verifica que el archivo subido tenga una extensión permitida
    según el tipo de contenido ('imagen' o 'archivo').
    """
    if "." not in nombre_archivo:
        return False
    extension = nombre_archivo.rsplit(".", 1)[1].lower()
    return extension in EXTENSIONES_PERMITIDAS.get(tipo, set())


def slugify_simple(texto: str) -> str:
    """
    Convierte un texto simple en un slug apto para URL.
    (Para nombres ya conocidos como los de grados/materias; para
    texto libre con acentos/ñ se recomienda usar una librería como
    python-slugify si se necesita generar slugs dinámicos).
    """
    return texto.strip().lower().replace(" ", "-")
