import dataclasses
import functools
import logging
import pprint
import time
from typing import Optional

import elasticsearch

from telethon.tl.types import UpdateNewChannelMessage, Channel, User, Photo
from elasticsearch.exceptions import ConnectionError

from sneaky_client.digest.digest import UpdateDigest
from sneaky_client.digest.photo_digest import PhotoDigest

log = logging.getLogger(__name__)


def is_none_or_bytes(x):
    if x is None:
        return True
    if isinstance(x, bytes):
        return True
    return False


def remove_none_and_binary(obj):
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none_and_binary(x) for x in obj if is_none_or_bytes(x))
    elif isinstance(obj, dict):
        return type(obj)(
            (remove_none_and_binary(k), remove_none_and_binary(v))
            for (k, v) in obj.items()
            if k is not None and not is_none_or_bytes(v)  # type: ignore
        )
    else:
        return obj


@functools.lru_cache()
def get_elasticsearch() -> elasticsearch.Elasticsearch:
    return wait_for_yellow_status(
        elasticsearch.Elasticsearch([{"host": "elastic", "port": 9200}])
    )


def wait_for_yellow_status(
    client: elasticsearch.Elasticsearch, nowait: bool = False, interval=5
) -> elasticsearch.Elasticsearch:
    for i in range(0, 1 if nowait else 100):
        try:
            client.cluster.health(wait_for_status="yellow")
            return client
        except ConnectionError:
            log.info(f"Waited {i * interval} seconds for Elastic Search to be live.")
            time.sleep(interval)
    else:
        # timeout
        raise RuntimeError("Elasticsearch failed to start.")


async def store_photo_record(photo: PhotoDigest):
    es = get_elasticsearch()
    es.index(
        index="photos",
        doc_type="photo",
        id=photo.id,
        body=remove_none_and_binary(dataclasses.asdict(photo)),
    )


def store(
    update: UpdateNewChannelMessage,
    user: Optional[User],
    channel: Channel,
    digest: UpdateDigest,
) -> None:
    es = get_elasticsearch()
    update_as_dict = update.to_dict()

    if "media" in update_as_dict["message"]:
        del update_as_dict["message"]["media"]

    update_id = hash((user.id if user else None, channel.id, update.message.id))

    es.index(
        index="updates",
        doc_type="update",
        id=update_id,
        body=remove_none_and_binary(update_as_dict),
    )
    es.index(
        index="channels",
        doc_type="channel",
        id=channel.id,
        body=remove_none_and_binary(channel.to_dict()),
    )
    if user:
        es.index(
            index="users",
            doc_type="user",
            id=user.id,
            body=remove_none_and_binary(user.to_dict()),
        )
    else:
        log.info("No user data available for this update.")

    digest_as_dict = remove_none_and_binary(dataclasses.asdict(digest))
    log.info(f"Saving message: {pprint.pformat(digest_as_dict)}")
    es.index(index="digests", doc_type="digest", id=digest.id, body=digest_as_dict)
    log.info(f"Finished saving #{update_id}")
