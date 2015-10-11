from urllib.parse import urljoin
from yatu.settings import API_BASE_URL


def make_uri(path):
    return urljoin(API_BASE_URL, path)