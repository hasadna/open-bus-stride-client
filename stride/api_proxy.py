import sys
import time
import subprocess
from contextlib import contextmanager

import psutil

from . import config, common


START_WAIT_TIME_INTERVAL = 0.05
START_WAIT_TIME_SECONDS = 15
START_WAIT_TIME_ITERATIONS = int(START_WAIT_TIME_SECONDS / START_WAIT_TIME_INTERVAL)


@contextmanager
def start(enable=True):
    """Start the API proxy server
    If enable is set to False, then the proxy server will not be started and stride client will run normally.
    This allows to use the contextmanager in any case.
    """
    if enable:
        STRIDE_API_BASE_URL = config.STRIDE_API_BASE_URL
        process = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'open_bus_stride_api.main:app', '--port', '0'])
        port = None
        try:
            for i in range(1, START_WAIT_TIME_ITERATIONS + 1):
                time.sleep(START_WAIT_TIME_INTERVAL)
                if port is None:
                    for connection in psutil.Process(process.pid).connections():
                        try:
                            port = connection.laddr.port
                            config.STRIDE_API_BASE_URL = f'http://localhost:{port}'
                            break
                        except:
                            if i >= START_WAIT_TIME_ITERATIONS:
                                raise
                    if i >= START_WAIT_TIME_ITERATIONS:
                        raise Exception("Failed to find port")
                if port is not None:
                    try:
                        common.get('/', params={})
                        break
                    except:
                        if i >= START_WAIT_TIME_ITERATIONS:
                            raise
            yield process
        finally:
            process.terminate()
            process.wait()
            config.STRIDE_API_BASE_URL = STRIDE_API_BASE_URL
    else:
        yield None
