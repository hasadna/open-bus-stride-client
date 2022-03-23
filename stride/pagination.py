from . import common


def iterate(path, params=None, limit=10000, pre_requests_callback=None):
    if not params:
        params = {}
    params['offset'] = 0
    while True:
        last_offset = params['offset']
        for obj in common.get(path, params=params, pre_requests_callback=pre_requests_callback):
            yield obj
            params['offset'] += 1
            if params['offset'] >= limit:
                break
        if params['offset'] == last_offset or params['offset'] >= limit:
            break
