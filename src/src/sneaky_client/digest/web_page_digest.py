from dataclasses import dataclass


@dataclass
class WebPageDigest:
    id: int
    title: str
    url: str
