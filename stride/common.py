import json
import datetime

import requests

from . import config, exceptions


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


def get(path, params=None):
    res = requests.get(config.STRIDE_API_BASE_URL + path, params=parse_params(params))
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
