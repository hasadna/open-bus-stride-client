import os
import json
from textwrap import dedent


import urbanaccess.gtfs.load
import urbanaccess.gtfs.network
import urbanaccess.osm.load
import urbanaccess.osm.network
import urbanaccess.network
import urbanaccess.plot


from .. import config
from ..common import create_unique_path


def main(fake_gtfs_path=None, fake_gtfs_kwargs=None, target_path=None):
    if fake_gtfs_kwargs:
        assert not fake_gtfs_path
        from .create_fake_gtfs import main
        fake_gtfs_path = main(**json.loads(fake_gtfs_kwargs))
    if not target_path:
        target_path = create_unique_path(os.path.join(config.OPEN_BUS_SIRI_ETL_ROOTPATH, 'urbanaccess'))
    assert os.path.exists(os.path.join(fake_gtfs_path, 'siri_feed', 'stop_times.txt'))
    assert os.path.exists(os.path.join(fake_gtfs_path, 'metadata.json'))
    print(dedent(f"""
        Creating urbanaccess network
        fake_gtfs_path={fake_gtfs_path}
        target_path={target_path}
    """))
    with open(os.path.join(fake_gtfs_path, 'metadata.json')) as f:
        fake_gtfs_metadata = json.load(f)
    start_hour = fake_gtfs_metadata['start_hour']
    end_hour = fake_gtfs_metadata['end_hour']
    bbox = tuple(fake_gtfs_metadata['bbox'])
    loaded_feeds = urbanaccess.gtfs.load.gtfsfeed_to_df(gtfsfeed_path=fake_gtfs_path)
    urbanaccess_net = urbanaccess.gtfs.network.create_transit_net(
        gtfsfeeds_dfs=loaded_feeds,
        day='tuesday',  # day doesn't matter because the fake gtfs data has service enabled for all days
        timerange=[f'{start_hour:02}:00:00', f'{end_hour:02}:00:00']
    )
    nodes, edges = urbanaccess.osm.load.ua_network_from_bbox(bbox=bbox, remove_lcn=True)
    urbanaccess.osm.network.create_osm_net(osm_edges=edges, osm_nodes=nodes, travel_speed_mph=3)
    urbanaccess.network.integrate_network(urbanaccess_network=urbanaccess_net, headways=False)
    urbanaccess.network.save_network(urbanaccess_network=urbanaccess_net, dir=target_path, filename='final_net.h5',
                                     overwrite_key=True)
    print(target_path)
    print('OK')
