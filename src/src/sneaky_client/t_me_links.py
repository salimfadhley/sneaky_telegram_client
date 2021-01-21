import logging
from typing import Iterator
import re

log = logging.getLogger(__name__)


def get_t_me_hashes(inp: str) -> Iterator[str]:
    """Given some text that contans hashes, return an iterator of hashes"""
    if not isinstance(inp, str):
        return []

    for match in re.findall("(telegram.me|t.me)(\/joinchat)?\/([a-zA-Z0-9\-_]+)", inp):
        yield match[2]

    for match in re.findall("(@[a-zA-Z0-9\-_]{3,})", inp):
        yield match
