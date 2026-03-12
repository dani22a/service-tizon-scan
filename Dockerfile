# ============================================
# Stage 1: Builder - dependencias
# ============================================
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Variables para compilación optimizada
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema necesarias para TensorFlow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# ============================================
# Stage 2: Runtime - imagen final
# ============================================
FROM python:3.11-slim-bookworm AS runtime

WORKDIR /app

# Usuario no-root para seguridad
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=4000

# Dependencias runtime: TensorFlow + OpenCV (inference_sdk/cv2 requiere libGL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copiar paquetes Python desde builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código de la aplicación
COPY --chown=appuser:appuser . .

# Crear directorio para archivos estáticos
RUN mkdir -p public && chown -R appuser:appuser public

USER appuser

EXPOSE 4000

# Gunicorn con workers uvicorn para producción
# --worker-tmp-dir /dev/shm evita "Permission denied" del control server en Docker
CMD ["sh", "-c", "gunicorn main:app -w ${WORKERS:-2} -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT} --timeout 120 --graceful-timeout 30 --worker-tmp-dir /dev/shm"]
