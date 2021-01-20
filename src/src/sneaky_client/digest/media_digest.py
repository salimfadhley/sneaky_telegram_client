import pprint
from dataclasses import dataclass
from typing import Optional
import logging

from telethon.tl.types import (
    MessageMediaDocument,
    WebPagePending,
    MessageMediaWebPage,
    WebPage,
    MessageMediaPhoto,
    MessageMediaContact,
)

from sneaky_client.digest.contact_digest import ContactDigest
from sneaky_client.digest.document_digest import DocumentDigest
from sneaky_client.digest.photo_digest import PhotoDigest
from sneaky_client.digest.web_page_digest import WebPageDigest


log = logging.getLogger(__name__)


@dataclass
class MediaDigest:
    photo: Optional[PhotoDigest] = None
    webpage: Optional[WebPageDigest] = None
    contact: Optional[ContactDigest] = None
    document: Optional[DocumentDigest] = None


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
    elif isinstance(media, WebPagePending):
        return MediaDigest(
            webpage=WebPageDigest(
                id=media.webpage.id, title="Unknown", url=media.webpage.url
            )
        )
    elif isinstance(media, MessageMediaWebPage) and isinstance(media.webpage, WebPage):
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
