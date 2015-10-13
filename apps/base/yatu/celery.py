from celery import Celery

from yatu import settings, bootstrap

bootstrap(settings)

app = Celery('yatu', broker=settings['amqp_conn_string'])
app.conf.update(**settings['celery_settings'])
app.autodiscover_tasks(['yatu.tasks'])
