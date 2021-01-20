from dataclasses import dataclass


@dataclass
class ChannelDigest:
    id: int
    title: str
    username: str
    megaroup: bool
    call_active: bool
