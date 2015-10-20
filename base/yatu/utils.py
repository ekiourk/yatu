from urllib.parse import urljoin
from yatu import settings


def make_uri(path):
    return urljoin(settings['api_base_url'], path)