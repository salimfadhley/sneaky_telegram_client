import datetime
from dataclasses import dataclass
from typing import Optional

from telethon.tl.types import MessageFwdHeader, PeerChannel, PeerChat


@dataclass
class ForwardDigest:
    date: datetime.datetime
    channel_id: Optional[int]
    chat_id: Optional[int]
    channel_post: Optional[int]
    from_name: Optional[str]
    post_author: Optional[str]


def get_fwd_digest(fwd: MessageFwdHeader) -> ForwardDigest:
    return ForwardDigest(
        date=fwd.date,
        channel_id=fwd.from_id.channel_id
        if isinstance(fwd.from_id, PeerChannel)
        else None,
        chat_id=fwd.from_id.chat_id if isinstance(fwd.from_id, PeerChat) else None,
        channel_post=fwd.channel_post,
        from_name=fwd.from_name,
        post_author=fwd.post_author,
    )
