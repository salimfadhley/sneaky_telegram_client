from dataclasses import dataclass


@dataclass
class ContactDigest:
    phone_number: str
    first_name: str
    last_name: str
    user_id: int
