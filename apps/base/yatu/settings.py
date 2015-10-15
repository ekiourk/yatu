from os import environ

POSTGRES_CONF = {
    'user': environ.get('POSTGRES_USER', 'yatu'),
    'pass': environ.get('POSTGRES_PASS', ''),
    'dbname': environ.get('POSTGRES_DBNAME', 'yatu'),
    'host': environ.get('DB_PORT_5432_TCP_ADDR', 'localhost'),
    'port': environ.get('DB_PORT_5432_TCP_PORT', '5432')
}

LOGGING_CONF = {
    "loggers": {
        "yatu": {
            "propagate": True,
            "level": "INFO"
        }
    },
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "formatter": "simpleFormatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": 0
        }
    },
    "root": {
        "level": 0,
        "handlers": [
            "console"
        ]
    },
    "formatters": {
        "simpleFormatter": {
            "datefmt": "%d/%m/%Y %H:%M:%S",
            "class": "logging.Formatter",
            "format": "%(asctime)s - %(name)s (%(levelname)s): %(message)s"
        }
    }
}

CELERY_CONF = {
    'CELERY_ALWAYS_EAGER': environ.get('CELERY_ALWAYS_EAGER', False)
}

settings = {
    'postgres_conf': POSTGRES_CONF,
    'postgres_conn_string': "postgres://{user}:{pass}@{host}:{port}/{dbname}".format(**POSTGRES_CONF),
    'api_base_url': environ.get('API_BASE_URL', 'http://localhost:8080'),
    'logging': LOGGING_CONF,
    'amqp_conn_string': 'amqp://guest:123@{host}//'.format(host=environ.get('RABBITMQ_PORT_5672_TCP_ADDR', 'localhost')),
    'celery_settings': CELERY_CONF
}