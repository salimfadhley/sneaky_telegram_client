import functools
import logging
from dataclasses import dataclass
from pathlib import Path

from telethon.errors import InviteHashInvalidError, FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import UpdateNewChannelMessage, Channel, User, MessageMediaPhoto

from sneaky_client.digest.digest import create_digest
from sneaky_client.digest.photo_digest import PhotoDigest
from sneaky_client.rabbit import EventQueue
from sneaky_client.storage import store, store_photo_record

log = logging.getLogger(__name__)

import os
from sneaky_client.config import get_config
from telethon import TelegramClient


@dataclass
class TelegramHandler:
    client: TelegramClient
    queue: EventQueue

    # This is our update handler. It is called when a new update arrives.
    async def handler(self, update):
        if isinstance(update, UpdateNewChannelMessage):
            await self.handle_update_new_channel_message(update)
        else:
            log.debug(f"Ignoring update: {update}")

    @functools.lru_cache()
    async def join_group(self, entity):
        """
        This looks bizarre, but I'm using lru_cache
        :param entity:
        :return:
        """
        log.info(f"Trying to join group/chat/channel: {entity}...")
        try:
            log.info(f"{entity} is not a hash, trying to subscribe as a group")
            channel: Channel = await self.client.get_entity(entity)
            return await self.client(JoinChannelRequest(channel))  # type: ignore
        except ValueError as e:
            log.info(f"{entity} is not a username, it might be a hash...")
            try:
                return await self.client(ImportChatInviteRequest(entity))
            except InviteHashInvalidError:
                log.warning(f"Could not subscribe to {entity}")
        except FloodWaitError:
            log.warning("Wait more time.")

    async def process_photo(self, update: UpdateNewChannelMessage):
        media: MessageMediaPhoto = update.message.media
        file_path: str = f"/content/photos/{media.photo.id}.jpg"

        if not os.path.exists(file_path):
            with open(file_path, "wb") as download_file:
                await self.client.download_media(message=update.message, file=file_path)

        photo_digest: PhotoDigest = PhotoDigest(
            id=media.photo.id, access_hash=media.photo.access_hash
        )

        await self.queue.notify_photo(photo_digest=photo_digest)
        await store_photo_record(photo=photo_digest)

        log.info(f"Saved photo: {file_path}, {os.path.getsize(file_path)} bytes")

    async def handle_update_new_channel_message(self, update: UpdateNewChannelMessage):
        channel: Channel = await self.client.get_entity(update.message.chat_id)

        if update.message.sender_id:
            try:
                _user = await self.client.get_entity(update.message.sender_id)
            except ValueError:
                _user = None
        else:
            _user = None

        user = _user if isinstance(_user, User) else None

        digest = create_digest(channel=channel, update=update, user=user)
        store(
            update=update,
            user=user if isinstance(user, User) else None,
            channel=channel,
            digest=digest,
        )

        if update.message.media and isinstance(update.message.media, MessageMediaPhoto):
            await self.process_photo(update)

        for entity in digest.entities:
            await self.join_group(entity)

        await self.client.send_read_acknowledge(entity=channel.id)


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
        queue = EventQueue(loop=client.loop)
        tg_handler = TelegramHandler(client=client, queue=queue)

        client.add_event_handler(tg_handler.handler)
        print("(Press Ctrl+C to stop this)")
        client.run_until_disconnected()
