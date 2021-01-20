from dataclasses import dataclass
import datetime
from typing import Optional, List
import logging


from telethon.tl.types import (
    UpdateNewChannelMessage,
    User,
    Channel,
)

from sneaky_client.digest.channel_digest import ChannelDigest
from sneaky_client.digest.fwd_digest import get_fwd_digest, ForwardDigest
from sneaky_client.digest.media_digest import MediaDigest, get_media_digest
from sneaky_client.digest.user_digest import UserDigest
from sneaky_client.t_me_links import get_t_me_hashes

log = logging.getLogger(__name__)


@dataclass
class MessageDigest:
    date: datetime.datetime
    message: str
    media: MediaDigest
    id: int


@dataclass
class UpdateDigest:
    user: Optional[UserDigest]
    channel: ChannelDigest
    message: MessageDigest
    entities: List[str]
    id: int
    fwd: Optional[ForwardDigest]


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
    channel_digest = ChannelDigest(
        id=channel.id,
        title=channel.title,
        username=channel.username,
        megaroup=channel.megagroup,
        call_active=channel.call_active,
    )

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
        fwd=get_fwd_digest(fwd=update.message.fwd_from)
        if update.message.fwd_from
        else None,  # This probably does not work
    )

    return update_digest
