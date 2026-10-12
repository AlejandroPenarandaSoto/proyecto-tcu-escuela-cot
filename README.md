# Proyecto TCU - Escuela Cot

Aplicación web educativa para la escuela, desarrollada con arquitectura **MVC** (Modelo-Vista-Controlador).

## Tecnologías

- **Backend:** Python + Flask
- **Frontend:** HTML, CSS, JavaScript (renderizado con Jinja2)
- **Base de datos:** SQLite (a través de SQLAlchemy como ORM)
- **Autenticación:** Flask-Login (solo para el módulo administrador)

## Módulos

1. **Módulo Estudiante** (público, sin inicio de sesión):
   - El estudiante elige su grado: Preescolar Interactivo, Preescolar Transición, Primero, Segundo, Tercero, Cuarto, Quinto, Sexto.
   - De Primero a Sexto, además elige la materia: Ciencias, Matemática, Español, Estudios Sociales, Inglés, Religión, Educación Musical, Educación Física.
   - Visualiza el contenido/material cargado por el administrador para esa combinación grado-materia.

2. **Módulo Administrador** (requiere usuario y contraseña):
   - Inicio de sesión.
   - CRUD del contenido/material que se muestra en cada grado y materia.

## Estructura del proyecto

```
proyecto-tcu-escuela-cot/
├── README.md
├── requirements.txt
├── .gitignore
├── config.py                 # Configuración de la app (Flask, BD, claves)
│
├── docs/                      # Documentación del proyecto
│
├── src/
│   ├── main.py                # Punto de entrada (app factory de Flask)
│   ├── model/                 # MODEL: entidades y reglas de negocio (SQLAlchemy)
│   ├── vista/                 # VIEW: templates HTML (Jinja2) + CSS + JS
│   ├── controller/            # CONTROLLER: Blueprints/rutas de Flask
│   ├── util/                  # UTIL: decoradores, validaciones
│   └── db/                    # DB: conexión, seed de datos iniciales, migraciones
│
└── tests/                     # Pruebas unitarias
```

## Instalación y ejecución

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Definir variables de entorno (opcional, ver config.py)
# En Windows (PowerShell): $env:FLASK_ENV="development"
export FLASK_ENV=development

# 4. Inicializar base de datos (crea tablas + datos iniciales de grados/materias)
python -m src.db.seed

# 5. Ejecutar la aplicación
python -m src.main
```

La aplicación quedará disponible en `http://127.0.0.1:5000`.

### Crear el primer usuario administrador

```bash
python -m src.db.crear_admin
```

Esto te pedirá un usuario y contraseña para el primer administrador del sistema.

## Rutas principales

| Ruta | Módulo | Descripción |
|---|---|---|
| `/` | Estudiante | Selección de grado |
| `/grado/<grado_slug>` | Estudiante | Selección de materia (o contenido directo si es preescolar) |
| `/grado/<grado_slug>/materia/<materia_slug>` | Estudiante | Contenido de esa materia y grado |
| `/admin/login` | Admin | Inicio de sesión |
| `/admin/dashboard` | Admin | Panel principal, listado de grados/materias |
| `/admin/contenido/<grado_id>/<materia_id>` | Admin | Editar contenido de un grado-materia |
| `/admin/logout` | Admin | Cerrar sesión |

## Próximos pasos sugeridos

- [ ] Definir tipos de contenido soportados (texto, PDF, video embebido, imágenes).
- [ ] Agregar subida de archivos (carpeta `uploads/` + validación de tipo/tamaño).
- [ ] Agregar tests en `tests/`.
- [ ] Documentación de usuario final en `docs/`.
