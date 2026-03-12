import logging
from datetime import date

from src.models import Periodo, User

logger = logging.getLogger("LOGGER SEED")


async def seed_periodos() -> None:
    users = await User.all()
    if not users:
        logger.warning("No hay usuarios para asociar periodos")
        return

    period_templates = [
        {
            "nombre": "Campana 2025-Temprana",
            "fecha_inicio": date(2025, 1, 15),
            "fecha_fin": date(2025, 4, 30),
            "descripcion": "Inicio de temporada con enfoque preventivo",
        },
        {
            "nombre": "Campana 2025-Tardia",
            "fecha_inicio": date(2025, 5, 1),
            "fecha_fin": date(2025, 8, 31),
            "descripcion": "Seguimiento de brotes durante mayor humedad",
        },
        {
            "nombre": "Campana 2026-Temprana",
            "fecha_inicio": date(2026, 1, 10),
            "fecha_fin": date(2026, 4, 20),
            "descripcion": "Campana de comparacion anual y control de calidad",
        },
    ]

    for user in users:
        for period_data in period_templates:
            periodo, created = await Periodo.get_or_create(
                usuario=user,
                nombre=period_data["nombre"],
                defaults={
                    "descripcion": period_data["descripcion"],
                    "fecha_inicio": period_data["fecha_inicio"],
                    "fecha_fin": period_data["fecha_fin"],
                },
            )

            if created:
                logger.info("Periodo creado: %s (%s)", periodo.nombre, user.email)
            else:
                periodo.descripcion = period_data["descripcion"]
                periodo.fecha_inicio = period_data["fecha_inicio"]
                periodo.fecha_fin = period_data["fecha_fin"]
                await periodo.save()
                logger.info("Periodo actualizado: %s (%s)", periodo.nombre, user.email)

    logger.info("Seeder de periodos completado")
