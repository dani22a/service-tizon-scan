# Service Tizon Scan - Levantar con Docker (DB externa)

Guia completa para ejecutar el backend con Docker en Windows, Linux o macOS,
cuando tu PostgreSQL ya esta desplegado en otro sitio (fuera de Docker).

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
- Tu PostgreSQL debe ser accesible desde el contenedor (red/puerto/credenciales)

Variables minimas recomendadas:

```env
PORT=4000
DEBUG=False
ENV=production

# Host/IP de TU PostgreSQL desplegado (desde el contenedor)
DB_HOST=host.docker.internal
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

Nota: `DB_HOST` debe ser el hostname o IP reales de tu base desplegada.
Si tu DB esta en otra maquina/servicio, usa ese host/IP y asegúrate de que el puerto (ej. `5432`) este abierto y accesible.

## 3) Construir imagen del backend

Desde la carpeta `service-tizon-scan`:

```bash
docker build -t service-tizon-scan:local .
```

## 4) Levantar backend en Docker

### Windows (PowerShell)

```bash
docker run -d --name service-tizon-scan `
  -p 4000:4000 `
  --env-file .env `
  service-tizon-scan:local
```

### Linux/macOS

```bash
docker run -d --name service-tizon-scan \
  -p 4000:4000 \
  --env-file .env \
  service-tizon-scan:local
```

## 5) Verificar que todo este arriba

```bash
docker ps
docker logs service-tizon-scan
```

La API debe responder en:

- `http://localhost:4000`
- `http://localhost:4000/docs`
- `http://localhost:4000/redoc`

## 6) Comandos utiles

Parar:

```bash
docker stop service-tizon-scan
```

Iniciar:

```bash
docker start service-tizon-scan
```

Eliminar y limpiar:

```bash
docker rm -f service-tizon-scan
```

## 7) Problemas comunes

- Si falla la conexion a DB:
  - valida que `.env` tenga el `DB_HOST`/`DB_PORT` correctos para tu PostgreSQL desplegado.
  - confirma que desde el contenedor se puede alcanzar el puerto de la DB (firewall, security group, DNS, etc.).
- Si el puerto `4000` esta ocupado:
  - cambia el mapeo `-p 4001:4000` y accede por `http://localhost:4001`.
