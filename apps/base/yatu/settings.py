from os import environ

POSTGRES_CONF = {
    'user': environ.get('POSTGRES_USER', 'yatu'),
    'pass': environ.get('POSTGRES_PASS', ''),
    'dbname': environ.get('POSTGRES_DBNAME', 'yatu'),
    'host': environ.get('POSTGRES_HOST', 'localhost'),
    'port': environ.get('POSTGRES_PORT', '5432')
}

settings = {
    'postgres_conf': POSTGRES_CONF,
    'postgres_conn_string': "postgres://{user}:{pass}@{host}:{port}/{dbname}".format(**POSTGRES_CONF),
    'api_base_url': environ.get('API_BASE_URL', 'http://localhost:8080')
}