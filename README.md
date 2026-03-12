# Crehana Backend Challenge

El foco estuvo en: diseño limpio de API, arquitectura por capas sencilla, uso de herramientas estándar en Python y un flujo de desarrollo razonable (tests, linters, Docker).

## Stack

- **Lenguaje**: Python 3.11
- **Framework**: FastAPI
- **BD**: PostgreSQL (app) + SQLite en memoria (tests)
- **ORM**: SQLAlchemy 2.x
- **Config**: Pydantic Settings
- **Auth**: JWT (python-jose + passlib)
- **Testing**: pytest
- **Calidad**: flake8, black, isort
- **Contenedores**: Docker + docker-compose

## Arquitectura (muy resumida)

- `app/domain`: modelos Pydantic, enums y excepciones de negocio.
- `app/application/services`: casos de uso (listas, tareas, auth).
- `app/infrastructure`:
  - `db`: configuración de SQLAlchemy, modelos y repositorios.
  - `auth`: helpers de JWT.
  - `config.py`: lectura de variables de entorno.
- `app/api/v1`: routers de FastAPI (auth, lists, tasks, health).
- `tests`: unitarios de servicios + integración end-to-end.

La idea es separar **dominio** de **framework** y **persistencia** para que sea fácil de testear y extender, sin sobre–ingeniería para un ejercicio acotado en tiempo.

## Casos de uso cubiertos

- CRUD de listas de tareas.
- CRUD de tareas dentro de una lista.
- Cambio de estado de tareas (`PENDING`, `IN_PROGRESS`, `DONE`).
- Listado de tareas con filtros por estado y prioridad.
- Cálculo de `%` de completitud por lista.
- Bonus:
  - Registro y login con JWT.
  - Asignación de tareas a usuarios.
  - Notificación ficticia al asignar (con `BackgroundTasks`).
  - Endpoint de health: `GET /api/v1/healthz`.

## Cómo ejecutar en local

Requisitos: Python 3.11, Postgres accesible o Docker si usas compose.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
cp .env.example .env  # ajustar valores si hace falta
uvicorn app.main:app --reload
```

- Swagger UI: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/api/v1/healthz`

## Docker / docker-compose

```bash
docker-compose up --build
# API: http://localhost:8000
# DB:  postgres://postgres:postgres@localhost:5432/crehana_db
```

## Tests y calidad

```bash
# Tests (unitarios + integración)
pytest

# Linter y formato
flake8 app tests
isort app tests
black app tests
```

También hay un `Makefile` con los comandos habituales:

```bash
make test      # pytest
make lint      # flake8
make format    # isort + black
make run       # uvicorn
make docker-up # docker-compose up --build
```


