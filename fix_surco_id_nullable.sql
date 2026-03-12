-- Permitir surco_id nulo en predicciones (el modelo Tortoise ya tiene null=True)
ALTER TABLE predicciones ALTER COLUMN surco_id DROP NOT NULL;
