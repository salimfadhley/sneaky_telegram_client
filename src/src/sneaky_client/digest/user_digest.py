from dataclasses import dataclass


@dataclass
class UserDigest:
    id: int
    name: str
    first_name: str
    last_name: str
    phone: str
    access_hash: int
