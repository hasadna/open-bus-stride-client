import os
import json
import datetime
import urllib.parse

import requests

from . import config, exceptions


def parse_value(v):
    if isinstance(v, str):
        if '-' in v and 'T' in v and ':' in v and '+' in v:
            if len(v) == 32:
                v = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f%z')
            elif len(v) == 25:
                v = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S%z')
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


def parse_error_res(res: dict):
    try:
        items = []
        message = res.pop('message', None)
        if message:
            items.append(message)
        traceback = res.pop('traceback', None)
        if traceback:
            items.append('\n'.join(traceback))
        if len(res) > 0:
            items.append(str(res))
        return '\n\n'.join(items)
    except:
        return res


def pre_requests_callback_print(url, params):
    if len(params) > 0:
        print('{}?{}'.format(url, urllib.parse.urlencode(params)))
    else:
        print(url)


def get(path, params=None, pre_requests_callback=None):
    url = config.STRIDE_API_BASE_URL + path
    params = parse_params(params)
    if pre_requests_callback:
        if pre_requests_callback == 'print':
            pre_requests_callback_print(url, params)
        else:
            pre_requests_callback(url, params)
    res = requests.get(url, params=params)
    res_status_code = res.status_code
    res_text = res.text
    if res_status_code == 200:
        try:
            res = json.loads(res_text)
        except json.JSONDecodeError:
            raise exceptions.StrideRequestParsingException(res_status_code, res_text)
        return parse_res(res)
    else:
        try:
            res = json.loads(res_text)
        except json.JSONDecodeError:
            raise exceptions.StrideRequestParsingException(res_status_code, res_text)
        raise exceptions.StrideRequestFailedException(
            res_status_code, res_text,
            msg="Failure response from Stride API ({}): {}".format(res_status_code, parse_error_res(res))
        )


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def create_unique_path(base_path, path_prefix=''):
    os.makedirs(base_path, exist_ok=True)
    for _ in range(5):
        path_part = '{}{}'.format(path_prefix, now().strftime('%Y-%m-%dT%H%M%S.%f'))
        path = os.path.join(base_path, path_part)
        try:
            os.mkdir(path)
        except FileExistsError:
            continue
        return path
    raise Exception("Failed to create unique path")


def is_None(val):
    # due to a problem with airflow dag initialization, in some cases we get
    # the actual string 'None' which we need to handle as None
    return val is None or val == 'None'


def parse_date_str(date, num_days=None):
    """Parses a date string in format %Y-%m-%d with default of today if empty
    if num_days is not None - will use a default of today minus given num_days
    """
    if isinstance(date, datetime.date):
        return date
    elif not date or is_None(date):
        return datetime.date.today() if num_days is None else datetime.date.today() - datetime.timedelta(days=int(num_days))
    else:
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
