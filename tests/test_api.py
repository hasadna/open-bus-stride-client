import datetime

import pytest

import stride
import stride.api_proxy

from .config import ALLOW_SLOW_TESTS


def get_siri_ride_stop_query_params():
    date = datetime.date(2022, 6, 21)
    min_lon, min_lat, max_lon, max_lat = 34.732918, 31.988688, 34.876007, 32.202171
    start_hour, end_hour = 8, 12
    recorded_at_time_from = datetime.datetime.combine(date, datetime.time(start_hour), datetime.timezone.utc)
    recorded_at_time_to = datetime.datetime.combine(date, datetime.time(end_hour, 59, 59), datetime.timezone.utc)
    return {
        'gtfs_stop__lat__greater_or_equal': min_lat,
        'gtfs_stop__lat__lower_or_equal': max_lat,
        'gtfs_stop__lon__greater_or_equal': min_lon,
        'gtfs_stop__lon__lower_or_equal': max_lon,
        'gtfs_date_from': date,
        'gtfs_date_to': date,
        'siri_vehicle_location__recorded_at_time_from': recorded_at_time_from,
        'siri_vehicle_location__recorded_at_time_to': recorded_at_time_to,
        'siri_ride__scheduled_start_time_from': recorded_at_time_from - datetime.timedelta(hours=10),
        'siri_ride__scheduled_start_time_to': recorded_at_time_to + datetime.timedelta(hours=10),
        'limit': -1,
    }


def assert_siri_ride_stop(s):
    assert isinstance(s, dict)
    assert isinstance(s['id'], int)
    assert isinstance(s['siri_ride__journey_ref'], str)
    assert isinstance(s['siri_ride__vehicle_ref'], str)
    assert isinstance(s['siri_ride__scheduled_start_time'], datetime.datetime)


@pytest.mark.skipif(not ALLOW_SLOW_TESTS, reason='slow test')
def test_streaming():
    num_stops = 0
    for siri_ride_stop in stride.iterate('/siri_ride_stops/list', params=get_siri_ride_stop_query_params(), limit=1050):
        assert_siri_ride_stop(siri_ride_stop)
        num_stops += 1
    assert num_stops == 1050


@pytest.mark.skipif(not ALLOW_SLOW_TESTS, reason='slow test')
def test_api_proxy_streaming():
    pytest.importorskip('open_bus_stride_api')
    with stride.api_proxy.start():
        num_stops = 0
        for siri_ride_stop in stride.iterate('/siri_ride_stops/list', params=get_siri_ride_stop_query_params(), limit=1050):
            assert_siri_ride_stop(siri_ride_stop)
            num_stops += 1
        assert num_stops == 1050


def test_iterate_get():
    siri_ride_stops = list(stride.iterate('/siri_ride_stops/list', params=get_siri_ride_stop_query_params(), limit=5))
    assert len(siri_ride_stops) == 5
    for siri_ride_stop in siri_ride_stops:
        assert_siri_ride_stop(siri_ride_stop)
    s = stride.get('/siri_ride_stops/get', {'id': siri_ride_stops[0]['id']})
    assert isinstance(s['id'], int)


def test_api_proxy_iterate_get():
    pytest.importorskip('open_bus_stride_api')
    with stride.api_proxy.start():
        siri_ride_stops = list(stride.iterate('/siri_ride_stops/list', params=get_siri_ride_stop_query_params(), limit=5))
        assert len(siri_ride_stops) == 5
        for siri_ride_stop in siri_ride_stops:
            assert_siri_ride_stop(siri_ride_stop)
        s = stride.get('/siri_ride_stops/get', {'id': siri_ride_stops[0]['id']})
        assert isinstance(s['id'], int)
