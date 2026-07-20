import logging

import dotenv
import uvicorn


dotenv.load_dotenv()

from src import create_app
from src.config import get_config


config = get_config()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = create_app()


if __name__ == "__main__":
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=config.PORT,
            log_level="info",
        )
    except Exception:
        logging.exception("No se pudo iniciar la aplicación")
        raise