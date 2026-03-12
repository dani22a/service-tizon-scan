-- ============================================================
-- Migración: Recomendaciones por predicción y nivel espacial
-- Fecha: 2026-03-06
-- ============================================================

-- ── Recomendaciones por predicción individual ────────────────────
CREATE TABLE IF NOT EXISTS prediccion_recommendations (
    id                  SERIAL PRIMARY KEY,
    usuario_id          INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    prediccion_id       INTEGER NOT NULL REFERENCES predicciones(id) ON DELETE CASCADE,
    categoria           VARCHAR(50)  NOT NULL,
    prioridad           VARCHAR(20)  NOT NULL,
    titulo              VARCHAR(255) NOT NULL,
    contenido           TEXT         NOT NULL,
    etiquetas           JSONB,
    metricas_snapshot   JSONB,
    fecha_creacion      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_at          TIMESTAMPTZ,
    updated_at          TIMESTAMPTZ,
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_prediccion_recommendations_prediccion
    ON prediccion_recommendations(prediccion_id);
CREATE INDEX IF NOT EXISTS idx_prediccion_recommendations_usuario
    ON prediccion_recommendations(usuario_id);

-- ── Diagnóstico por SURCO ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS surco_reports (
    id                              SERIAL PRIMARY KEY,
    usuario_id                      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    surco_id                        INTEGER NOT NULL REFERENCES surcos(id) ON DELETE CASCADE,
    total_predicciones              INTEGER     NOT NULL,
    con_enfermedad                  INTEGER     NOT NULL,
    saludables                      INTEGER     NOT NULL,
    confianza_promedio              FLOAT       NOT NULL,
    total_detecciones               INTEGER     NOT NULL,
    promedio_detecciones_por_imagen FLOAT       NOT NULL,
    tasa_consenso                   FLOAT       NOT NULL,
    indice_severidad                FLOAT       NOT NULL,
    tendencia                       VARCHAR(30) NOT NULL,
    enfermedad_predominante         VARCHAR(100),
    distribucion_enfermedades       JSONB,
    fecha_reporte                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at                      TIMESTAMPTZ,
    updated_at                      TIMESTAMPTZ,
    deleted_at                      TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_surco_reports_surco ON surco_reports(surco_id);

CREATE TABLE IF NOT EXISTS surco_recommendations (
    id             SERIAL PRIMARY KEY,
    usuario_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    surco_id       INTEGER NOT NULL REFERENCES surcos(id) ON DELETE CASCADE,
    report_id      INTEGER NOT NULL REFERENCES surco_reports(id) ON DELETE CASCADE,
    categoria      VARCHAR(50)  NOT NULL,
    prioridad      VARCHAR(20)  NOT NULL,
    titulo         VARCHAR(255) NOT NULL,
    contenido      TEXT         NOT NULL,
    etiquetas      JSONB,
    fecha_creacion TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_at     TIMESTAMPTZ,
    updated_at     TIMESTAMPTZ,
    deleted_at     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_surco_recommendations_surco  ON surco_recommendations(surco_id);
CREATE INDEX IF NOT EXISTS idx_surco_recommendations_report ON surco_recommendations(report_id);

-- ── Diagnóstico por LOTE ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS lote_reports (
    id                              SERIAL PRIMARY KEY,
    usuario_id                      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lote_id                         INTEGER NOT NULL REFERENCES lotes(id) ON DELETE CASCADE,
    total_predicciones              INTEGER     NOT NULL,
    con_enfermedad                  INTEGER     NOT NULL,
    saludables                      INTEGER     NOT NULL,
    confianza_promedio              FLOAT       NOT NULL,
    total_detecciones               INTEGER     NOT NULL,
    promedio_detecciones_por_imagen FLOAT       NOT NULL,
    tasa_consenso                   FLOAT       NOT NULL,
    indice_severidad                FLOAT       NOT NULL,
    tendencia                       VARCHAR(30) NOT NULL,
    enfermedad_predominante         VARCHAR(100),
    surcos_monitoreados             JSONB,
    distribucion_enfermedades       JSONB,
    fecha_reporte                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at                      TIMESTAMPTZ,
    updated_at                      TIMESTAMPTZ,
    deleted_at                      TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_lote_reports_lote ON lote_reports(lote_id);

CREATE TABLE IF NOT EXISTS lote_recommendations (
    id             SERIAL PRIMARY KEY,
    usuario_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lote_id        INTEGER NOT NULL REFERENCES lotes(id) ON DELETE CASCADE,
    report_id      INTEGER NOT NULL REFERENCES lote_reports(id) ON DELETE CASCADE,
    categoria      VARCHAR(50)  NOT NULL,
    prioridad      VARCHAR(20)  NOT NULL,
    titulo         VARCHAR(255) NOT NULL,
    contenido      TEXT         NOT NULL,
    etiquetas      JSONB,
    fecha_creacion TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_at     TIMESTAMPTZ,
    updated_at     TIMESTAMPTZ,
    deleted_at     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_lote_recommendations_lote   ON lote_recommendations(lote_id);
CREATE INDEX IF NOT EXISTS idx_lote_recommendations_report ON lote_recommendations(report_id);

-- ── Diagnóstico por MÓDULO ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS modulo_reports (
    id                              SERIAL PRIMARY KEY,
    usuario_id                      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    modulo_id                       INTEGER NOT NULL REFERENCES modulos(id) ON DELETE CASCADE,
    total_predicciones              INTEGER     NOT NULL,
    con_enfermedad                  INTEGER     NOT NULL,
    saludables                      INTEGER     NOT NULL,
    confianza_promedio              FLOAT       NOT NULL,
    total_detecciones               INTEGER     NOT NULL,
    promedio_detecciones_por_imagen FLOAT       NOT NULL,
    tasa_consenso                   FLOAT       NOT NULL,
    indice_severidad                FLOAT       NOT NULL,
    tendencia                       VARCHAR(30) NOT NULL,
    enfermedad_predominante         VARCHAR(100),
    lotes_monitoreados              JSONB,
    surcos_monitoreados             JSONB,
    distribucion_enfermedades       JSONB,
    fecha_reporte                   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at                      TIMESTAMPTZ,
    updated_at                      TIMESTAMPTZ,
    deleted_at                      TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_modulo_reports_modulo ON modulo_reports(modulo_id);

CREATE TABLE IF NOT EXISTS modulo_recommendations (
    id             SERIAL PRIMARY KEY,
    usuario_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    modulo_id      INTEGER NOT NULL REFERENCES modulos(id) ON DELETE CASCADE,
    report_id      INTEGER NOT NULL REFERENCES modulo_reports(id) ON DELETE CASCADE,
    categoria      VARCHAR(50)  NOT NULL,
    prioridad      VARCHAR(20)  NOT NULL,
    titulo         VARCHAR(255) NOT NULL,
    contenido      TEXT         NOT NULL,
    etiquetas      JSONB,
    fecha_creacion TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    created_at     TIMESTAMPTZ,
    updated_at     TIMESTAMPTZ,
    deleted_at     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_modulo_recommendations_modulo  ON modulo_recommendations(modulo_id);
CREATE INDEX IF NOT EXISTS idx_modulo_recommendations_report  ON modulo_recommendations(report_id);
