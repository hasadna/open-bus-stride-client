import requests

from . import config


def get(path, params=None):
    return requests.get(config.STRIDE_API_BASE_URL + path, params=params).json()
