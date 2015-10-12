from os import environ

POSTGRES_CONF = {
    'user': environ.get('POSTGRES_USER', 'yatu'),
    'pass': environ.get('POSTGRES_PASS', ''),
    'dbname': environ.get('POSTGRES_DBNAME', 'yatu'),
    'host': environ.get('POSTGRES_HOST', 'localhost'),
    'port': environ.get('POSTGRES_PORT', '5432')
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

settings = {
    'postgres_conf': POSTGRES_CONF,
    'postgres_conn_string': "postgres://{user}:{pass}@{host}:{port}/{dbname}".format(**POSTGRES_CONF),
    'api_base_url': environ.get('API_BASE_URL', 'http://localhost:8080'),
    'logging': LOGGING_CONF
}