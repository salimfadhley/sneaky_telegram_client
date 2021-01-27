import dataclasses
import functools
import json
import logging
from asyncio import SelectorEventLoop
from dataclasses import dataclass, asdict

import aio_pika
from aio_pika import RobustConnection, RobustChannel

from sneaky_client.digest.photo_digest import PhotoDigest

log = logging.getLogger(__name__)


def encode_dataclass(d) -> bytes:
    return json.dumps(asdict(d)).encode()


@dataclass
class EventQueue:
    loop: SelectorEventLoop

    async def get_connection(self) -> RobustConnection:
        return await aio_pika.connect_robust(
            "amqp://guest:guest@rabbit/", loop=self.loop
        )

    async def get_channel(self) -> RobustChannel:
        connection = await self.get_connection()
        return await connection.channel()

    async def notify_photo(self, photo_digest: PhotoDigest, routing_key="photos"):
        channel = await self.get_channel()

        result = await channel.default_exchange.publish(
            aio_pika.Message(body=encode_dataclass(photo_digest)),
            routing_key=routing_key,
        )
        log.info(f"Notifying phtoto: {photo_digest}, got result {result}")

        await channel.close()
