import json

import requests
import json_stream
import json_stream.base
import json_stream.requests


from . import config, common, exceptions


def iterate(path, params=None, limit=10000, pre_requests_callback=None):
    if not params:
        params = {}
    url = config.STRIDE_API_BASE_URL + path
    params = common.parse_params(params)
    if pre_requests_callback:
        if pre_requests_callback == 'print':
            common.pre_requests_callback_print(url, params)
        else:
            pre_requests_callback(url, params)
    with requests.get(url, params=params, stream=True) as res:
        res_status_code = res.status_code
        if res_status_code == 200:
            data = json_stream.requests.load(res)
            for i, item in enumerate(data):
                if isinstance(item, json_stream.base.TransientStreamingJSONObject):
                    item = {k: v for k, v in item.items()}
                elif isinstance(item, json_stream.base.TransientStreamingJSONList):
                    item = [v for v in item]
                yield common.parse_res(item)
                if limit and i+1 >= limit:
                    break
        else:
            res_text = res.text
            try:
                res = json.loads(res_text)
            except json.JSONDecodeError:
                raise exceptions.StrideRequestParsingException(res_status_code, res_text)
            raise exceptions.StrideRequestFailedException(
                res_status_code, res_text,
                msg="Failure response from Stride API ({}): {}".format(res_status_code, common.parse_error_res(res))
            )
