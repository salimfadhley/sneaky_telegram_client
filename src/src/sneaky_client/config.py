from dataclasses import dataclass

import yaml


@dataclass
class Config:
    app_api_id: str
    app_api_hash: str
    phone_number: str
    encryption_key: str

def get_config() -> Config:
    with open("/config/simpleclient/config.yaml") as f:
        return Config(**yaml.safe_load(f))
