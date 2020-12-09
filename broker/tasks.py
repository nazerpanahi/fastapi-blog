from __future__ import absolute_import, unicode_literals

from elasticsearch import Elasticsearch

from broker.celery import app
from conf.settings import ELASTICSEARCH_SETTINGS

db = Elasticsearch()


@app.task()
def save_data_in_elastic(data: dict, index='default'):
    db.index(index=index, body=data)
    return data
