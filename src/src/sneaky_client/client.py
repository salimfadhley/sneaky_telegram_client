from telegram.client import Telegram

from client.config import get_config


def run_client():
    config = get_config()
    tg = Telegram(
        api_id=config.app_api_id,
        api_hash=config.app_api_hash,
        phone=config.phone_number,
        database_encryption_key=config.encryption_key,
    )

    tg.login()
