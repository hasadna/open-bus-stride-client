import datetime

import pytest

import stride


def assert_siri_ride_stop(s):
    assert isinstance(s, dict)
    assert isinstance(s['id'], int)
    assert isinstance(s['siri_ride__journey_ref'], str)
    assert isinstance(s['siri_ride__vehicle_ref'], str)
    assert isinstance(s['siri_ride__scheduled_start_time'], datetime.datetime)


@pytest.mark.skip('too slow')
def test_streaming():
    num_stops = 0
    for siri_ride_stop in stride.iterate('/siri_ride_stops/list', limit=10000):
        assert_siri_ride_stop(siri_ride_stop)
        num_stops += 1
    assert num_stops == 10000


def test_iterate_get():
    siri_ride_stops = list(stride.iterate('/siri_ride_stops/list', limit=5))
    assert len(siri_ride_stops) == 5
    for siri_ride_stop in siri_ride_stops:
        assert_siri_ride_stop(siri_ride_stop)
    s = stride.get('/siri_ride_stops/get', {'id': siri_ride_stops[0]['id']})
    assert isinstance(s['id'], int)
