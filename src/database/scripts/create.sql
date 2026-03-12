
CREATE DATABASE db_model_potato;

\c db_model_potato;

-- 1. users
CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    username    VARCHAR(20)  NOT NULL UNIQUE,
    password    TEXT         NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    full_name   VARCHAR(255) DEFAULT NULL,
    created_at  TIMESTAMPTZ  DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  DEFAULT NOW(),
    deleted_at  TIMESTAMPTZ  DEFAULT NULL
);

-- 2. modulos
CREATE TABLE IF NOT EXISTS modulos (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(255) NOT NULL,
    descripcion TEXT         DEFAULT NULL,
    user_id     INT          NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ  DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  DEFAULT NOW(),
    deleted_at  TIMESTAMPTZ  DEFAULT NULL
);

-- 3. lotes
CREATE TABLE IF NOT EXISTS lotes (
    id            SERIAL PRIMARY KEY,
    identificador VARCHAR(100) NOT NULL,
    descripcion   TEXT         DEFAULT NULL,
    modulo_id     INT          NOT NULL REFERENCES modulos(id) ON DELETE CASCADE,
    created_at    TIMESTAMPTZ  DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  DEFAULT NOW(),
    deleted_at    TIMESTAMPTZ  DEFAULT NULL,
    UNIQUE (modulo_id, identificador)
);

-- 4. surcos
CREATE TABLE IF NOT EXISTS surcos (
    id          SERIAL PRIMARY KEY,
    numero      INT  NOT NULL,
    descripcion TEXT DEFAULT NULL,
    lote_id     INT  NOT NULL REFERENCES lotes(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW(),
    deleted_at  TIMESTAMPTZ DEFAULT NULL,
    UNIQUE (lote_id, numero)
);

-- 5. predicciones
CREATE TABLE IF NOT EXISTS predicciones (
    id             SERIAL PRIMARY KEY,
    surco_id       INT          DEFAULT NULL REFERENCES surcos(id) ON DELETE CASCADE,
    usuario_id     INT          DEFAULT NULL REFERENCES users(id) ON DELETE CASCADE,
    imagen_url     TEXT         DEFAULT NULL,
    fase1_resumen  JSONB        DEFAULT NULL,
    fase1_payload  JSONB        DEFAULT NULL,
    fase2_resumen  JSONB        DEFAULT NULL,
    fase2_payload  JSONB        DEFAULT NULL,
    fecha          TIMESTAMPTZ  DEFAULT NOW(),
    created_at     TIMESTAMPTZ  DEFAULT NOW(),
    updated_at     TIMESTAMPTZ  DEFAULT NOW(),
    deleted_at     TIMESTAMPTZ  DEFAULT NULL
);

-- ============================================================
-- Índices
-- ============================================================

CREATE INDEX idx_modulos_user_id           ON modulos(user_id);
CREATE INDEX idx_lotes_modulo_id           ON lotes(modulo_id);
CREATE INDEX idx_surcos_lote_id            ON surcos(lote_id);
CREATE INDEX idx_predicciones_surco_id     ON predicciones(surco_id);
CREATE INDEX idx_predicciones_usuario_id   ON predicciones(usuario_id);
CREATE INDEX idx_predicciones_fecha        ON predicciones(fecha DESC);
