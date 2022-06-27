import os
import json
import datetime
from pprint import pprint
from textwrap import dedent
from collections import defaultdict
from contextlib import contextmanager

from .. import config, iterate, api_proxy
from ..common import create_unique_path, parse_date_str


def gtfs_escape(val):
    return val.replace(',', '').replace('\n', ' ')


def create_calendar(target_path, date: datetime.date):
    service_id = '1'
    with open(os.path.join(target_path, 'calendar.txt'), 'w') as f:
        f.writelines([
            'service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\n',
            f'{service_id},1,1,1,1,1,1,1,{date.strftime("%Y%m%d")},{date.strftime("%Y%m%d")}\n'
        ])
    return service_id


@contextmanager
def open_files(target_path):
    with open(os.path.join(target_path, 'stops.txt'), 'w') as f_stops:
        with open(os.path.join(target_path, 'routes.txt'), 'w') as f_routes:
            with open(os.path.join(target_path, 'trips.txt'), 'w') as f_trips:
                with open(os.path.join(target_path, 'stop_times.txt'), 'w') as f_stop_times:
                    yield f_stops, f_routes, f_trips, f_stop_times


def create_data(
        stats, target_path, service_id, date, start_hour, end_hour,
        min_lon, min_lat, max_lon, max_lat,
        use_proxy_server, limit_stop_times
):
    added_stop_ids = set()
    added_route_ids = set()
    added_trip_ids = set()
    with open_files(target_path) as (f_stops, f_routes, f_trips, f_stop_times):
        f_stops.write('stop_id,stop_name,stop_lat,stop_lon,location_type\n',)
        f_routes.write('route_id,route_short_name,route_type\n')
        f_trips.write('route_id,service_id,trip_id\n')
        f_stop_times.write('trip_id,arrival_time,departure_time,stop_id,stop_sequence\n')
        recorded_at_time_from = datetime.datetime.combine(date, datetime.time(start_hour), datetime.timezone.utc)
        recorded_at_time_to = datetime.datetime.combine(date, datetime.time(end_hour, 59, 59), datetime.timezone.utc)
        with api_proxy.start(use_proxy_server):
            for item in iterate('/siri_ride_stops/list', {
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
            }, limit=None):
                svl_recorded_at_time = item['nearest_siri_vehicle_location__recorded_at_time'].strftime("%H:%M:%S")
                gs_name = gtfs_escape(f'{item["gtfs_stop__city"]}: {item["gtfs_stop__name"]}')
                gs_id = item['gtfs_stop_id']
                if gs_id not in added_stop_ids:
                    added_stop_ids.add(gs_id)
                    f_stops.write(f'{gs_id},{gs_name},{item["gtfs_stop__lat"]},{item["gtfs_stop__lon"]},0\n')
                    stats['stops'] += 1
                grt_id = item['gtfs_ride__gtfs_route_id']
                if grt_id not in added_route_ids:
                    added_route_ids.add(grt_id)
                    f_routes.write(f'{grt_id},{gtfs_escape(item["gtfs_route__route_short_name"])},3\n')
                    stats['routes'] += 1
                gr_id = item['siri_ride__gtfs_ride_id']
                if gr_id not in added_trip_ids:
                    added_trip_ids.add(gr_id)
                    f_trips.write(f'{grt_id},{service_id},{gr_id}\n')
                    stats['trips'] += 1
                f_stop_times.write(f'{gr_id},{svl_recorded_at_time},{svl_recorded_at_time},{gs_id},{item["order"]}\n')
                stats['stop_times'] += 1
                if stats["stop_times"] > 1 and stats["stop_times"] % 1000 == 0:
                    print(f'saved {stats["stop_times"]} stop times...')
                if limit_stop_times and stats["stop_times"] >= limit_stop_times:
                    break


def main(date, start_hour, end_hour, bbox, target_path=None, use_proxy_server=False, limit_stop_times=None):
    if not target_path:
        target_path = create_unique_path(os.path.join(config.URBANACCESS_DATA_PATH, 'fake_gtfs'))
    target_path_feed = os.path.join(target_path, 'siri_feed')
    os.makedirs(target_path_feed)
    date = parse_date_str(date)
    start_hour = int(start_hour)
    end_hour = int(end_hour)
    min_lon, min_lat, max_lon, max_lat = [float(v.strip()) for v in bbox.split(',')]
    print(dedent(f'''
        creating fake gtfs data
        target_path={target_path}
        date: {date}
        hours: {start_hour} - {end_hour}
        bbox: {min_lon},{min_lat} - {max_lon},{max_lat}
    '''))
    stats = defaultdict(int)
    service_id = create_calendar(target_path_feed, date)
    create_data(
        stats, target_path_feed, service_id, date, start_hour, end_hour,
        min_lon, min_lat, max_lon, max_lat,
        use_proxy_server, limit_stop_times
    )
    with open(os.path.join(target_path, 'metadata.json'), 'w') as f:
        json.dump({
            'start_hour': start_hour,
            'end_hour': end_hour,
            'bbox': [min_lon, min_lat, max_lon, max_lat]
        }, f)
    pprint(dict(stats))
    print(f'Fake gtfs data successfully stored at "{target_path}"')
    return target_path
