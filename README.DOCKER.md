# Service Tizon Scan - Levantar con Docker

Guia completa para ejecutar el backend con Docker en Windows, Linux o macOS.

## 1) Instalar Docker

### Windows (recomendado)
1. Descarga Docker Desktop desde:
   - [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Instala Docker Desktop y reinicia si lo solicita.
3. Abre Docker Desktop y espera a que diga "Engine running".
4. Verifica en terminal:

```bash
docker --version
docker compose version
```

### Linux (resumen)
1. Instala Docker Engine segun tu distribucion:
   - [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
2. (Opcional) agrega tu usuario al grupo docker.
3. Verifica:

```bash
docker --version
```

## 2) Requisitos del proyecto

- Estar ubicado en `service-tizon-scan`
- Tener un archivo `.env` en la raiz (si no existe, crealo)

Variables minimas recomendadas:

```env
PORT=4000
DEBUG=False
ENV=production

DB_HOST=postgres
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

Nota: `DB_HOST=postgres` es importante porque el backend y Postgres correran en la misma red de Docker.

## 3) Crear red Docker (una sola vez)

```bash
docker network create tizon-net
```

Si ya existe, Docker mostrara un mensaje y puedes continuar.

## 4) Levantar PostgreSQL en Docker

```bash
docker run -d --name tizon-postgres ^
  --network tizon-net ^
  -e POSTGRES_USER=postgres ^
  -e POSTGRES_PASSWORD=postgres ^
  -e POSTGRES_DB=db_model_potato ^
  -p 5432:5432 ^
  postgres:16
```

En Linux/macOS usa `\` en vez de `^` para salto de linea.

## 5) Construir imagen del backend

Desde la carpeta `service-tizon-scan`:

```bash
docker build -t service-tizon-scan:local .
```

## 6) Levantar backend en Docker

```bash
docker run -d --name service-tizon-scan ^
  --network tizon-net ^
  --env-file .env ^
  -p 4000:4000 ^
  service-tizon-scan:local
```

## 7) Verificar que todo este arriba

```bash
docker ps
docker logs service-tizon-scan
```

La API debe responder en:

- `http://localhost:4000`
- `http://localhost:4000/docs`
- `http://localhost:4000/redoc`

## 8) Comandos utiles

Parar contenedores:

```bash
docker stop service-tizon-scan tizon-postgres
```

Iniciarlos de nuevo:

```bash
docker start tizon-postgres service-tizon-scan
```

Eliminar y limpiar:

```bash
docker rm -f service-tizon-scan tizon-postgres
docker network rm tizon-net
```

## 9) Problemas comunes

- Si falla la conexion a DB:
  - confirma que `tizon-postgres` esta en ejecucion.
  - valida que `.env` tenga `DB_HOST=postgres`.
- Si el puerto `4000` esta ocupado:
  - cambia el mapeo `-p 4001:4000` y accede por `http://localhost:4001`.
- Si el puerto `5432` esta ocupado:
  - cambia el mapeo `-p 5433:5432` (internamente la app sigue usando `5432` hacia `postgres`).
