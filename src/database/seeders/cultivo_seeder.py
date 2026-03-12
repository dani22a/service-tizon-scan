import logging

from src.models import Lote, Modulo, Surco, User

logger = logging.getLogger("LOGGER SEED")


async def seed_cultivo() -> None:
    users = await User.all()
    if not users:
        logger.warning("No hay usuarios para asociar modulos/lotes/surcos")
        return

    for user in users:
        modulo_specs = [
            {
                "nombre": "Modulo Norte",
                "descripcion": "Zona con mayor humedad y monitoreo preventivo",
                "lotes": [
                    {"identificador": "N-01", "descripcion": "Lote experimental norte 1", "surcos": 8},
                    {"identificador": "N-02", "descripcion": "Lote experimental norte 2", "surcos": 10},
                ],
            },
            {
                "nombre": "Modulo Centro",
                "descripcion": "Zona de produccion principal",
                "lotes": [
                    {"identificador": "C-01", "descripcion": "Lote comercial centro 1", "surcos": 12},
                    {"identificador": "C-02", "descripcion": "Lote comercial centro 2", "surcos": 12},
                ],
            },
            {
                "nombre": "Modulo Sur",
                "descripcion": "Zona de rotacion y control de rendimiento",
                "lotes": [
                    {"identificador": "S-01", "descripcion": "Lote de seguimiento sur 1", "surcos": 6},
                ],
            },
        ]

        for modulo_spec in modulo_specs:
            modulo, modulo_created = await Modulo.get_or_create(
                nombre=modulo_spec["nombre"],
                user=user,
                defaults={"descripcion": modulo_spec["descripcion"]},
            )
            if modulo_created:
                logger.info("Modulo creado: %s (%s)", modulo.nombre, user.email)
            else:
                modulo.descripcion = modulo_spec["descripcion"]
                await modulo.save()
                logger.info("Modulo actualizado: %s (%s)", modulo.nombre, user.email)

            for lote_spec in modulo_spec["lotes"]:
                lote, lote_created = await Lote.get_or_create(
                    modulo=modulo,
                    identificador=lote_spec["identificador"],
                    defaults={"descripcion": lote_spec["descripcion"]},
                )
                if lote_created:
                    logger.info("Lote creado: %s", lote.identificador)
                else:
                    lote.descripcion = lote_spec["descripcion"]
                    await lote.save()
                    logger.info("Lote actualizado: %s", lote.identificador)

                for numero in range(1, lote_spec["surcos"] + 1):
                    surco, created_surco = await Surco.get_or_create(
                        lote=lote,
                        numero=numero,
                        defaults={"descripcion": f"Surco {numero} de {lote.identificador}"},
                    )
                    if not created_surco and not surco.descripcion:
                        surco.descripcion = f"Surco {numero} de {lote.identificador}"
                        await surco.save()

        logger.info("Seeder de cultivo aplicado para: %s", user.email)
