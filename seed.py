from src.database.seeders import seed_database
import asyncio
import logging

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("LOGGER SEED")

async def main():
  await seed_database()
  logger.info("Database seeded successfully")

asyncio.run(main())