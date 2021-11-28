import datetime

import requests

from . import config


def parse_value(v):
    if isinstance(v, str):
        if len(v) == 32 and '-' in v and 'T' in v and ':' in v and '+' in v:
            v = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f%z')
    return v


def parse_res(res):
    if isinstance(res, dict):
        for k, v in res.items():
            res[k] = parse_value(v)
    elif isinstance(res, list):
        for item in res:
            parse_res(item)
    return res


def parse_params(params):
    for k, v in params.items():
        if isinstance(v, datetime.datetime):
            if not v.tzinfo:
                raise TypeError('timezone info is required for date/time values')
            params[k] = v.astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    return params


def get(path, params=None):
    return parse_res(requests.get(config.STRIDE_API_BASE_URL + path, params=parse_params(params)).json())
