import dataclasses
import logging
import pprint
from typing import Optional

import elasticsearch

from telethon.tl.types import UpdateNewChannelMessage, Channel, User, Photo

from sneaky_client.digest.digest import UpdateDigest
from sneaky_client.digest.photo_digest import PhotoDigest

log = logging.getLogger(__name__)


def remove_none(obj):
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
        return type(obj)(
            (remove_none(k), remove_none(v))
            for k, v in obj.items()
            if k is not None and v is not None
        )
    else:
        return obj


def get_elasticsearch() -> elasticsearch.Elasticsearch:
    return elasticsearch.Elasticsearch([{"host": "elastic", "port": 9200}])


async def store_photo_record(photo: PhotoDigest):
    es = get_elasticsearch()
    es.index(
        index="photos", doc_type="photo", id=photo.id, body=dataclasses.asdict(photo)
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
        body=remove_none(update_as_dict),
    )
    es.index(
        index="channels",
        doc_type="channel",
        id=channel.id,
        body=remove_none(channel.to_dict()),
    )
    if user:
        es.index(
            index="users", doc_type="user", id=user.id, body=remove_none(user.to_dict())
        )
    else:
        log.info("No user data available for this update.")

    digest_as_dict = remove_none(dataclasses.asdict(digest))
    log.info(f"Saving message: {pprint.pformat(digest_as_dict)}")
    es.index(index="digests", doc_type="digest", id=digest.id, body=digest_as_dict)
    log.info(f"Finished saving #{update_id}")
