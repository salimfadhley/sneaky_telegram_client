from dataclasses import dataclass
import datetime
from typing import Optional, List
import pprint
import logging


from telethon.tl.types import (
    UpdateNewChannelMessage,
    User,
    Channel,
    MessageMediaDocument,
    MessageMediaWebPage,
    MessageMediaPhoto,
    MessageMediaContact,
)

from sneaky_client.t_me_links import get_t_me_hashes

log = logging.getLogger(__name__)


@dataclass
class UserDigest:
    id: int
    name: str
    first_name: str
    last_name: str
    phone: str
    access_hash: int


@dataclass
class ChannelDigest:
    id: int
    name: str


@dataclass
class DocumentDigest:
    id: int
    access_hash: int
    size: int


@dataclass
class PhotoDigest:
    id: int
    access_hash: int


@dataclass
class WebPageDigest:
    id: int
    title: str
    url: str


@dataclass
class ContactDigest:
    phone_number: str
    first_name: str
    last_name: str
    user_id: int


@dataclass
class MediaDigest:
    photo: Optional[PhotoDigest] = None
    webpage: Optional[WebPageDigest] = None
    contact: Optional[ContactDigest] = None
    document: Optional[DocumentDigest] = None


@dataclass
class MessageDigest:
    date: datetime.datetime
    message: str
    media: MediaDigest
    id: int


def get_media_digest(media) -> MediaDigest:
    log.info(f"Got media: {media}")
    if not media:
        return MediaDigest()
    elif isinstance(media, MessageMediaDocument):
        return MediaDigest(
            document=DocumentDigest(
                id=media.document.id,
                access_hash=media.document.access_hash,
                size=media.document.size,
            )
        )
    elif isinstance(media, MessageMediaWebPage):
        return MediaDigest(
            webpage=WebPageDigest(
                id=media.webpage.id, title=media.webpage.title, url=media.webpage.url
            )
        )
    elif isinstance(media, MessageMediaPhoto):
        return MediaDigest(
            photo=PhotoDigest(id=media.photo.id, access_hash=media.photo.access_hash)
        )
    elif isinstance(media, MessageMediaContact):
        return MediaDigest(
            contact=ContactDigest(
                user_id=media.user_id,
                first_name=media.first_name,
                last_name=media.last_name,
                phone_number=media.phone_number,
            )
        )
    else:
        log.info(f"Cannot handle {media.__class__}: {pprint.pformat(media)}")
        return MediaDigest()


@dataclass
class UpdateDigest:
    user: Optional[UserDigest]
    channel: ChannelDigest
    message: MessageDigest
    entities: List[str]
    id: int


def get_user_digest(user: User) -> UserDigest:
    return UserDigest(
        id=user.id,
        name=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        access_hash=user.access_hash,
    )


def create_digest(
    update: UpdateNewChannelMessage, user: Optional[User], channel: Channel
) -> UpdateDigest:
    channel_digest = ChannelDigest(id=channel.id, name=channel.title)

    user_digest: Optional[UserDigest] = get_user_digest(user) if user else None

    message_digest = MessageDigest(
        id=update.message.id,
        message=update.message.message,
        media=get_media_digest(update.message.media),
        date=update.message.date,
    )

    hashable_identifiers = (
        channel_digest.id,
        user_digest.id if user_digest else None,
        message_digest.id,
    )

    entities: List[str] = (
        list(get_t_me_hashes(message_digest.message)) if message_digest.message else []
    )

    update_digest = UpdateDigest(
        user=user_digest,
        channel=channel_digest,
        message=message_digest,
        id=hash(hashable_identifiers),
        entities=entities,
    )

    return update_digest
