import logging
from sneaky_client.client import run_client

log = logging.getLogger(__name__)

def start():
    logging.basicConfig()
    logging.getLogger("").setLevel(logging.INFO)
    log.info("Client starting")
    try:
        run_client()
    finally:
        log.info("Client ending.")

if __name__ == "__main__":
    start()
