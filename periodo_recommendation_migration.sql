-- Migración: tablas para reportes y recomendaciones de periodos
-- Ejecutar contra la base de datos existente

-- ── Tabla de reportes de periodo ─────────────────────────────────
-- Snapshot completo de métricas en el momento en que se generaron
-- las recomendaciones. Permite reconstruir el contexto histórico.
CREATE TABLE IF NOT EXISTS periodo_reports (
    id                              SERIAL PRIMARY KEY,
    usuario_id                      INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    periodo_id                      INTEGER NOT NULL REFERENCES periodos(id) ON DELETE CASCADE,

    -- métricas generales
    total_predicciones              INTEGER NOT NULL DEFAULT 0,
    con_enfermedad                  INTEGER NOT NULL DEFAULT 0,
    saludables                      INTEGER NOT NULL DEFAULT 0,
    confianza_promedio              FLOAT   NOT NULL DEFAULT 0.0,
    total_detecciones               INTEGER NOT NULL DEFAULT 0,
    promedio_detecciones_por_imagen FLOAT   NOT NULL DEFAULT 0.0,
    tasa_consenso                   FLOAT   NOT NULL DEFAULT 0.0,

    -- métricas temporales
    dias_activos                    INTEGER NOT NULL DEFAULT 0,
    frecuencia_monitoreo            FLOAT   NOT NULL DEFAULT 0.0,

    -- severidad / tendencia
    indice_severidad                FLOAT   NOT NULL DEFAULT 0.0,
    tendencia                       VARCHAR(30) NOT NULL DEFAULT 'insuficiente_datos',
    enfermedad_predominante         VARCHAR(100) NULL,

    -- cobertura espacial y distribución detallada (contexto de las recomendaciones)
    surcos_monitoreados             JSONB NULL,
    distribucion_enfermedades       JSONB NULL,

    fecha_reporte                   TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at                      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at                      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at                      TIMESTAMP WITH TIME ZONE NULL
);

CREATE INDEX IF NOT EXISTS idx_periodo_reports_periodo_id
    ON periodo_reports (periodo_id);
CREATE INDEX IF NOT EXISTS idx_periodo_reports_usuario_id
    ON periodo_reports (usuario_id);

-- ── Tabla de recomendaciones de periodo ──────────────────────────
-- Cada recomendación está vinculada a su report (snapshot de métricas)
-- y al periodo al que pertenece.
CREATE TABLE IF NOT EXISTS periodo_recommendations (
    id              SERIAL PRIMARY KEY,
    usuario_id      INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    periodo_id      INTEGER NOT NULL REFERENCES periodos(id) ON DELETE CASCADE,
    report_id       INTEGER NOT NULL REFERENCES periodo_reports(id) ON DELETE CASCADE,

    categoria       VARCHAR(50)  NOT NULL,   -- fungicida | monitoreo | riego | general | alerta
    prioridad       VARCHAR(20)  NOT NULL,   -- urgente | alta | media | baja
    titulo          VARCHAR(255) NOT NULL,
    contenido       TEXT         NOT NULL,
    etiquetas       JSONB NULL,

    fecha_creacion  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at      TIMESTAMP WITH TIME ZONE NULL
);

CREATE INDEX IF NOT EXISTS idx_periodo_recommendations_periodo_id
    ON periodo_recommendations (periodo_id);
CREATE INDEX IF NOT EXISTS idx_periodo_recommendations_report_id
    ON periodo_recommendations (report_id);
CREATE INDEX IF NOT EXISTS idx_periodo_recommendations_usuario_id
    ON periodo_recommendations (usuario_id);
