import os
import glob
import tempfile
import datetime

import pytest

import stride.urbanaccess.create_fake_gtfs
import stride.urbanaccess.create_network

from .config import ALLOW_SLOW_TESTS


@pytest.mark.skipif(not ALLOW_SLOW_TESTS, reason='slow test')
def test_create_network_fake_gtfs_data():
    try:
        import open_bus_stride_api
        use_proxy_server = True
    except ImportError:
        use_proxy_server = False
    date = datetime.date(2022, 6, 21)
    min_lon, min_lat, max_lon, max_lat = 34.875169, 32.078883, 34.8804, 32.085137
    start_hour, end_hour = 8, 9
    bbox = ','.join(map(str, [min_lon, min_lat, max_lon, max_lat]))
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_gtfs_path = os.path.join(tmpdir, 'fake_gtfs')
        stride.urbanaccess.create_fake_gtfs.main(
            date, start_hour, end_hour, bbox, target_path=fake_gtfs_path, use_proxy_server=use_proxy_server,
            limit_stop_times=5
        )
        filenames = {filename.split('/')[-1] for filename in glob.glob(f'{fake_gtfs_path}/**/*.txt', recursive=True)}
        assert filenames == {
            "trips.txt",
            "stops.txt",
            "routes.txt",
            "calendar.txt",
            "stop_times.txt"
        }
        for filename in filenames:
            assert os.path.getsize(os.path.join(fake_gtfs_path, 'siri_feed', filename)) > 0
        network_path = os.path.join(tmpdir, 'network')
        stride.urbanaccess.create_network.main(fake_gtfs_path=fake_gtfs_path, target_path=network_path)


