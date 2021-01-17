import itertools
import logging
import os
from pathlib import Path
import elasticsearch

import yaml
from telethon.tl.types import UpdateUserStatus

log = logging.getLogger(__name__)


def get_elasticsearch()->elasticsearch.Elasticsearch:
    return elasticsearch.Elasticsearch([{'host': 'elastic', 'port': 9200}])

def store(obj:UpdateUserStatus)->None:
    es = get_elasticsearch()
    update_as_dict = obj.to_dict()
    log.info(f"Saving update:\n{update_as_dict}")
    es.index(index='nutters', doc_type='update', body=update_as_dict)
