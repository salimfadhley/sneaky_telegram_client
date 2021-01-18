import logging
from dataclasses import dataclass
from typing import Optional

from telethon.tl.types import UpdateNewChannelMessage, Channel, User

from sneaky_client.message_digest import create_digest
from sneaky_client.storage import store

log = logging.getLogger(__name__)

import os
from sneaky_client.config import get_config
from telethon import TelegramClient


@dataclass
class TelegramHandler:
    client: TelegramClient

    # This is our update handler. It is called when a new update arrives.
    async def handler(self, update):
        if isinstance(update, UpdateNewChannelMessage):
            channel: Channel = await self.client.get_entity(update.message.chat_id)
            _user = await self.client.get_entity(update.message.sender_id)
            user = _user if isinstance(_user, User) else None

            digest = create_digest(channel=channel, update=update, user=user)
            store(
                update=update,
                user=user if isinstance(user, User) else None,
                channel=channel,
                digest=digest,
            )
        else:
            log.info(f"Ignoring update: {update}")


def get_session_path() -> str:
    session_dir = os.environ["SESSION_LOCATION"]
    session_path = os.path.join(session_dir, "sneaky.session")
    log.info(f"Saving session to {session_path}")
    return session_path


def run_client():
    config = get_config()
    api_id = config.app_api_id
    api_hash = config.app_api_hash

    with TelegramClient(get_session_path(), api_id, api_hash) as client:
        tg_handler = TelegramHandler(client=client)

        client.add_event_handler(tg_handler.handler)

        # Run the client until Ctrl+C is pressed, or the client disconnects
        print("(Press Ctrl+C to stop this)")
        client.run_until_disconnected()
