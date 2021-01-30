import functools
from typing import Callable

import rollbar
import sneaky_client

from sneaky_client.config import get_config


def initialize_rollbar() -> None:
    config = get_config()
    rollbar.init(
        get_config().rollbar_id,
        environment=config.rollbar_environment_name,
        code_version=sneaky_client.__version__,
    )


def exception_catching_decorator():
    def deco(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args):
            try:
                return await func(*args)
            except Exception as e:
                rollbar.report_exc_info()
                raise

        return wrapped

    return deco
