import logging
from typing import Iterator
import re

log = logging.getLogger(__name__)


def get_t_me_hashes(inp: str) -> Iterator[str]:
    """Given some text that contans hashes, return an iterator of hashes"""
    try:
        matches = re.findall("(telegram.me|t.me)(\/joinchat)?\/([a-zA-Z0-9\-_]+)", inp)
    except TypeError:
        log.exception(f"Cannot get entity codes from {inp.__class__}: {inp}")
        return iter([])
    for match in matches:
        yield match[2]
