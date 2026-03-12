-- SQL to apply when running against an existing database
-- create table periodos and add nullable periodo_id to predicciones

CREATE TABLE IF NOT EXISTS periodos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE predicciones
    ADD COLUMN IF NOT EXISTS periodo_id INTEGER NULL REFERENCES periodos(id) ON DELETE SET NULL;
