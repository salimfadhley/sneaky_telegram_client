import os
from dataclasses import dataclass

import yaml


@dataclass
class Config:
    app_api_id: int
    app_api_hash: str
    phone_number: str
    encryption_key: str


def get_config() -> Config:
    with open(os.path.expanduser("~/.config/simpleclient/config.yaml")) as f:
        config = yaml.safe_load(f)
        assert isinstance(config["app_api_id"], int)
        assert isinstance(config["app_api_hash"], str)
        assert isinstance(config["phone_number"], str)
        assert isinstance(config["encryption_key"], str)

        return Config(**config)

if __name__ == "__main__":
    print(get_config())
