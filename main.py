import dotenv

dotenv.load_dotenv()

from src import create_app
from src.config import get_config
import uvicorn
import logging

config = get_config()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    try:
        app =  create_app()
        uvicorn.run(app, port=config.PORT, log_level="info")
    except Exception as e:
        logging.error(e)
        exit(1)