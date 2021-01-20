import logging
import os

from sneaky_client.client import run_client

log = logging.getLogger(__name__)


def ensure_directories_exist() -> None:
    os.makedirs("/content/photos", exist_ok=True)


def start():
    logging.basicConfig()
    logging.getLogger("").setLevel(logging.INFO)
    log.info("Client starting")
    ensure_directories_exist()
    try:
        run_client()
    finally:
        log.info("Client ending.")


if __name__ == "__main__":
    start()
