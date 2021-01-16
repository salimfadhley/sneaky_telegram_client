import itertools
import logging
import os
from pathlib import Path
from typing import Any, Mapping

import yaml

log = logging.getLogger(__name__)


def get_storage_path()->Path:
    p = Path(os.environ["STORAGE_LOCATION"])
    assert p.exists(), f"Storage location ${p} does not exist"
    assert p.is_dir(), f"Storage location ${p} is not a directory/"
    return p

counter = itertools.count()

def store(obj:Mapping[str,Any])->None:
    count = next(counter)
    storage_path = get_storage_path().joinpath(f"{count}.yaml")
    with storage_path.open(mode="w") as f:
        log.info(f"Dunping {storage_path}")
        yaml.dump(obj, f)
