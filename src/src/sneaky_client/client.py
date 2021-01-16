from dataclasses import dataclass

from sneaky_client.config import get_config
from telegram.client import Telegram

import logging

from sneaky_client.storage import store

log = logging.getLogger(__name__)




@dataclass
class TelegramClient:
    tg: Telegram


    def lookup_chat(self, chat_id:int):
        self.tg.call_method()

    def new_message_handler(self, update):


        chat = self.lookup_chat(update["message"]["chat_id"])

        store(update)




def run_client():
    config = get_config()
    tg = Telegram(
        api_id=config.app_api_id,
        api_hash=config.app_api_hash,
        phone=config.phone_number,
        database_encryption_key=config.encryption_key,
    )

    tg.login()

    client = TelegramClient(tg=tg)

    tg.add_message_handler(client.new_message_handler)

    tg.idle()
