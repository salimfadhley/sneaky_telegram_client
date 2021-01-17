from dataclasses import dataclass
import datetime
from typing import Optional, Union
import pprint
import logging


from telethon.tl.types import UpdateNewChannelMessage, User, Channel, MessageMediaDocument, MessageMediaWebPage, \
    MessageMediaPhoto, MessageMediaContact

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
    access_hash: int


@dataclass
class MediaDigest:
    id: int
    type: str
    title: str
    description: str
    display_url: str
    url: str


@dataclass
class MessageDigest:
    date: datetime.datetime
    message: str
    media: MediaDigest
    id: int




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
    last_nane: str
    user_id: int


@dataclass
class MediaDigest:
    photo: Optional[PhotoDigest]=None
    webpage: Optional[WebPageDigest]=None
    contact: Optional[ContactDigest]=None
    document: Optional[DocumentDigest]=None

def get_media_digest(media)->MediaDigest:
    log.info(f"Got media: {media}")
    if not media:
        return None
    elif isinstance(media, MessageMediaDocument):
        return MediaDigest(document=DocumentDigest(
            id = media.document.id,
            access_hash=media.document.access_hash,
            size=media.document.size
        ))
    elif isinstance(media, MessageMediaWebPage):
        return MediaDigest(webpage=WebPageDigest(
            id=media.webpage.id,
            title=media.webpage.title,
            url=media.webpage.url
        ))
    elif isinstance(media, MessageMediaPhoto):
        return MediaDigest(photo=PhotoDigest(
            id = media.photo.id,
            access_hash=media.photo.access_hash
        ))
    elif isinstance(media, MessageMediaContact):
        return MediaDigest(contact=ContactDigest(
            user_id=media.contact.user_id,
            first_name=media.contact.first_name,
            last_name=media.contact.last_name,
            phone_number=media.contact.phone_number
        ))
    else:
        log.info(f"Cannot handle {media.__class__}: {pprint.pprint(media)}")
        return MediaDigest()



@dataclass
class UpdateDigest:
    user: UserDigest
    channel: ChannelDigest
    message: MessageDigest
    id: int

def create_digest(update:UpdateNewChannelMessage, user:User, channel:Channel)->UpdateDigest:
    channel_digest = ChannelDigest(
        id = channel.id,
        name = channel.title,
        access_hash = channel.access_hash,
    )

    user_digest = UserDigest(
        id = user.id,
        name=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        access_hash=user.access_hash
    )

    message_digest = MessageDigest(
        id = update.message.id,
        message = update.message.message,
        media = get_media_digest(update.message.media),
        date = update.message.date
    )

    hashable_identifiers = (channel_digest.id, user_digest.id, message_digest.id)

    update_digest = UpdateDigest(
        user = user_digest,
        channel = channel_digest,
        message= message_digest,
        id = hash(hashable_identifiers)
    )

    return update_digest
