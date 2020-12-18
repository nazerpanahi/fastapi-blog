from __future__ import absolute_import, unicode_literals

from broker.celery import app
from utils.db_utils import get_elasticsearch_db


@app.task()
def save_data_in_elastic(data: dict, index='default'):
    get_elasticsearch_db().index(index=index, body=data)
    return data
