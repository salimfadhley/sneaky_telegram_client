import logging
from dataclasses import dataclass
from typing import Optional

from telethon.errors import InviteHashInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import UpdateNewChannelMessage, Channel, User, InputChannel

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
            await self.handle_update_new_channel_message(update)

        else:
            log.info(f"Ignoring update: {update}")

    async def subscribe_to_entity(self, entity):
        try:
            subscription_result = await self.client(ImportChatInviteRequest(entity))
        except InviteHashInvalidError:
            log.info(f"{entity} is not a hash, trying to subscribe as a group")
            channel: Channel = await self.client.get_entity(entity)
            subscription_result = await self.client(JoinChannelRequest(channel))  # type: ignore
        log.info(f"Subscription result for {entity} is {subscription_result}")
        return subscription_result

    async def handle_update_new_channel_message(self, update: UpdateNewChannelMessage):
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

        for entity in digest.entities:
            await self.subscribe_to_entity(entity)


def get_session_path() -> str:
    session_dir = os.environ["SESSION_LOCATION"]
    session_path = os.path.join(session_dir, "sneaky.session")
    log.info(f"Saving session to {session_path}")
    return session_path


def get_telegram_client() -> TelegramClient:
    config = get_config()
    api_id = config.app_api_id
    api_hash = config.app_api_hash
    return TelegramClient(get_session_path(), api_id, api_hash)


def run_client():
    with get_telegram_client() as client:
        tg_handler = TelegramHandler(client=client)

        client.add_event_handler(tg_handler.handler)

        # Run the client until Ctrl+C is pressed, or the client disconnects
        print("(Press Ctrl+C to stop this)")
        client.run_until_disconnected()
