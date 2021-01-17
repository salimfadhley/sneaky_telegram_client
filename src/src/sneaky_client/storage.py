import dataclasses
import logging
import pprint
from typing import Optional

import elasticsearch

from telethon.tl.types import UpdateNewChannelMessage, Channel, User

from sneaky_client.message_digest import create_digest

log = logging.getLogger(__name__)


def get_elasticsearch() -> elasticsearch.Elasticsearch:
    return elasticsearch.Elasticsearch([{"host": "elastic", "port": 9200}])


def store(
    update: UpdateNewChannelMessage, user: Optional[User], channel: Channel
) -> None:
    es = get_elasticsearch()
    update_as_dict = update.to_dict()

    if "media" in update_as_dict["message"]:
        del update_as_dict["message"]["media"]

    update_id = hash((user.id if user else None, channel.id, update.message.id))

    es.index(index="updates", doc_type="update", id=update_id, body=update_as_dict)
    es.index(
        index="channels", doc_type="channel", id=channel.id, body=channel.to_dict()
    )
    if user:
        es.index(index="users", doc_type="user", id=user.id, body=user.to_dict())

    digest = create_digest(user=user, channel=channel, update=update)
    digest_as_dict = dataclasses.asdict(digest)
    log.info(f"Saving message: {pprint.pformat(digest_as_dict)}")
    es.index(index="digests", doc_type="digest", id=digest.id, body=digest_as_dict)
