# Potato Disease Classification API

API REST para clasificación de enfermedades de la papa usando TensorFlow/Keras. Desarrollada con FastAPI, Tortoise ORM y autenticación JWT.

## Requisitos Previos

- Python 3.12+
- PostgreSQL 12+
- pip o pipenv

## Instalación

1. Clonar el repositorio y entrar al directorio:

```bash
cd service_model
```

2. Crear entorno virtual:

```bash
python -m venv venv
```

3. Activar entorno virtual:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

1. Crear archivo `.env` en la raíz del proyecto:

```env
PORT=4000
DEBUG=True
ENV=development

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=root
DB_NAME=db_model_potato

JWT_SECRET="tu_secret_key_aqui"
JWT_EXPIRATION=3600

DOMAIN=.localhost
NAME_COOKIE=token_access

ROBOFLOW_API_URL=https://serverless.roboflow.com
ROBOFLOW_API_KEY=tu_api_key_roboflow
ROBOFLOW_MODEL_ID=potato_late_blight_yolov8n/10
ROBOFLOW_TIMEOUT_SEC=15
MAX_IMAGE_SIZE_MB=10
```

2. Asegurarse de que PostgreSQL esté corriendo y crear la base de datos:

```sql
CREATE DATABASE db_model_potato;
```

## Estructura del Proyecto

```
service_model/
├── src/
│   ├── config/          # Configuraciones (DB, JWT, Tortoise)
│   ├── controllers/     # Endpoints de la API
│   ├── database/        # Conexión y seeders
│   ├── helpers/         # Funciones auxiliares
│   ├── lib/             # Utilidades (JWT, bcrypt)
│   ├── middleware/      # Middleware de autenticación JWT
│   ├── models/          # Modelos de DB y ML (classifier)
│   ├── schemas/         # Esquemas Pydantic para validación
│   └── services/        # Lógica de negocio
├── model/               # Modelo entrenado (.keras) y métricas
├── main.py              # Punto de entrada
├── seed.py              # Script para poblar DB
└── requirements.txt     # Dependencias
```

## Ejecución

1. Poblar la base de datos (opcional, solo primera vez):

```bash
python seed.py
```

2. Iniciar el servidor:

```bash
python main.py
```

3. La API estará disponible en: `http://localhost:4000`

4. Documentación interactiva:
   - Swagger UI: `http://localhost:4000/docs`
   - ReDoc: `http://localhost:4000/redoc`

## Endpoints Principales

### Autenticación (Públicos)

- `POST /api/v1/login` - Iniciar sesión
  ```json
  {
    "email": "usuario@ejemplo.com",
    "password": "123456"
  }
  ```

### Evaluación (Protegido)

- `POST /api/v1/evaluation/evaluate` - Clasificar imagen de papa
  - Form-data: `file` (imagen)
  - Header: `Authorization: Bearer <token>`

- `POST /api/v1/evaluation/roboflow` - Inferencia con modelo hosted en Roboflow
  - Header: `Authorization: Bearer <token>`
  - Opcion 1 (archivo): Form-data `file` (imagen)
  - Opcion 2 (URL): Form-data `image_url` (http/https)

Ejemplo de respuesta (cuando hay detecciones):

```json
{
  "data": {
    "source": "file",
    "model_id": "potato_late_blight_yolov8n/10",
    "predictions": [
      {
        "x": 174.5,
        "y": 46.5,
        "width": 123,
        "height": 97,
        "confidence": 0.707,
        "class": "blight",
        "class_id": 0,
        "detection_id": "81f1cf32-d08e-4922-bd21-e26b19de03ac"
      }
    ],
    "has_matches": true
  },
  "status": "success",
  "message": "Roboflow inference successful"
}
```

Si `predictions` llega vacio, la inferencia se considera exitosa sin coincidencias.

## Nuevas tablas y migraciones

Al agregar el módulo de periodos se añade una tabla `periodos` y se crea una columna
`periodo_id` (nullable) en `predicciones`.
Para bases existentes ejecuta el script `periodo_migration.sql` o genera esquemas con
`Tortoise.generate_schemas()` en un entorno de desarrollo.  

Nota: `generate_schemas()` no actualiza tablas existentes, sólo crea nuevas; por ello se
provee SQL manual para añadir `periodo_id` si ya hay datos.

### Entrenamiento (Protegido)

- `POST /api/v1/train/*` - Endpoints de entrenamiento del modelo

## Autenticación

Todas las rutas excepto `/login` requieren autenticación JWT.

**Enviar token:**

- Header: `Authorization: Bearer <token>`
- Query param: `?token=<token>`

El token se obtiene del endpoint `/login` en la respuesta:

```json
{
  "data": {
    "token": "eyJ..."
  },
  "status": "success",
  "message": "Login successful"
}
```

## Scripts Útiles

- `python seed.py` - Poblar base de datos con datos iniciales completos:
  - Usuarios
  - Módulos
  - Lotes
  - Surcos
  - Períodos
- `python create_tables.py` - Crear tablas manualmente (si generate_schemas falla)
- `python check_postgres.py` - Verificar conexión a PostgreSQL

## Notas

- El modelo de ML debe estar en `model/model.keras`
- Las métricas y configuración del modelo en `model/metrics.json`
- En desarrollo, las cookies no usan `secure=True` (solo HTTP)
- El middleware JWT protege automáticamente todas las rutas excepto las públicas
