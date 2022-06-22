import click


@click.group()
def urbanaccess():
    """Run accessibility analysis using UrbanAccess"""
    pass


@urbanaccess.command()
@click.option('--target-path')
@click.option('--date')
@click.option('--start-hour')
@click.option('--end-hour')
@click.option('--bbox', help='comma-separated square bounding box values: min_lon, min_lat, max_lon, max_lat. '
                             'Can get it from https://boundingbox.klokantech.com/ - csv export')
def create_fake_gtfs(**kwargs):
    """Create fake GTFS data from the siri data to use as input to UrbanAccess"""
    from .create_fake_gtfs import main
    main(**kwargs)


@urbanaccess.command()
@click.option('--target-path')
@click.option('--fake-gtfs-path', help='path to output of create-fake-gtfs task')
@click.option('--fake-gtfs-kwargs', help='json of create-fake-gtfs task arguments')
def create_network(**kwargs):
    """Create UrbanAccess accessibility network from the fake gtfs data"""
    from .create_urbanaccess_network import main
    main(**kwargs)
