from celery import Celery
from celery.task import task
import inject

from yatu import settings

app = Celery('yatu', broker=settings['amqp_conn_string'])
app.conf.update(**settings['celery_settings'])


@task
def increase_visits_count(sid):
    uow = inject.instance('UnitOfWorkManager')
    with uow.start() as tx:
        short_url = tx.short_urls.get(sid)
        if short_url:
            short_url.increase_visits()
            tx.commit()
