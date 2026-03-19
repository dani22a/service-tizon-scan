# Service Tizon Scan - Levantar sin Docker

Guia completa para ejecutar el backend localmente con Python + PostgreSQL.

## 1) Instalar Python

Version recomendada para este proyecto: **Python 3.11.x**.

### Windows
1. Descarga Python 3.11 desde:
   - [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Durante la instalacion marca **Add Python to PATH**.
3. Verifica:

```bash
python --version
pip --version
```

### Linux/macOS
Instala Python 3.11 con tu gestor de paquetes o `pyenv`, luego verifica:

```bash
python3 --version
pip3 --version
```

## 2) Instalar PostgreSQL

1. Descarga PostgreSQL (12+):
   - [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
2. Crea una base de datos para el proyecto:

```sql
CREATE DATABASE db_model_potato;
```

## 3) Crear y activar entorno virtual

Desde `service-tizon-scan`:

```bash
python -m venv .venv
```

Activar:

```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat

# Linux/macOS
source .venv/bin/activate
```

## 4) Instalar dependencias

```bash
pip install -r requirements.txt
```

## 5) Configurar variables de entorno

Crea o ajusta el archivo `.env` en la raiz del proyecto:

```env
PORT=4000
DEBUG=True
ENV=development

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=db_model_potato

JWT_SECRET=tu_secret_super_seguro
JWT_EXPIRATION=3600
DOMAIN=.localhost
NAME_COOKIE=token_access

CORS_ORIGINS=http://localhost:3000

ROBOFLOW_API_URL=https://serverless.roboflow.com
ROBOFLOW_API_KEY=
ROBOFLOW_MODEL_ID=
ROBOFLOW_TIMEOUT_SEC=15
MAX_IMAGE_SIZE_MB=10
```

## 6) Levantar el backend

```bash
python main.py
```

La API quedara disponible en:

- `http://localhost:4000`
- `http://localhost:4000/docs`
- `http://localhost:4000/redoc`

## 7) Seed de datos (opcional)

Con el entorno virtual activo:

```bash
python seed.py
```

## 8) Pruebas (opcional)

```bash
pytest
```

## 9) Problemas comunes

- Error de conexion a DB:
  - revisa usuario/password/puerto en `.env`.
  - confirma que PostgreSQL este iniciado.
- Error al activar entorno virtual en PowerShell:
  - habilita ejecucion de scripts para tu usuario:
    - `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Si `python` apunta a otra version:
  - en Windows prueba `py -3.11 -m venv .venv`.
