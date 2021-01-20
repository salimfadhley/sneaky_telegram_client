from dataclasses import dataclass


@dataclass
class DocumentDigest:
    id: int
    access_hash: int
    size: int
