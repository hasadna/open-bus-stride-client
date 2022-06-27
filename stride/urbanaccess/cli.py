import click


@click.group()
def urbanaccess():
    """Run accessibility analysis using UrbanAccess"""
    pass


@urbanaccess.command()
@click.option('--target-path', help="Target path to save the fake gtfs data to. "
                                    "If not provided will create a unique path in local directory.")
@click.option('--date', help="Date string in format %Y-%m-%d, for example: \"2022-06-15\"", required=True)
@click.option('--start-hour', type=int, required=True, help="UTC Hour")
@click.option('--end-hour', type=int, required=True, help="UTC Hour")
@click.option('--bbox', help='comma-separated square bounding box values: min_lon, min_lat, max_lon, max_lat. '
                             'For example: "34.8, 31.96, 34.81, 31.97". '
                             'Can get it from https://boundingbox.klokantech.com/ - csv export',
              required=True)
@click.option('--use-proxy-server', is_flag=True)
def create_fake_gtfs(**kwargs):
    """Create fake GTFS data from the siri data to use as input to UrbanAccess"""
    from .create_fake_gtfs import main
    main(**kwargs)


@urbanaccess.command()
@click.option('--target-path')
@click.option('--fake-gtfs-path', help='path to output of create-fake-gtfs task. '
                                       'If provided, the other fake gtfs arguments are not needed.')
@click.option('--date', help="To create fake gtfs data - date string in format %Y-%m-%d, for example: \"2022-06-15\"")
@click.option('--start-hour', type=int, help="To create fake gtfs data - UTC Hour")
@click.option('--end-hour', type=int, help="To create fake gtfs data - UTC Hour")
@click.option('--bbox', help='To create fake gtfs data - comma-separated square bounding box values: min_lon, min_lat, max_lon, max_lat. '
                             'For example: "34.8, 31.96, 34.81, 31.97". '
                             'Can get it from https://boundingbox.klokantech.com/ - csv export')
def create_network(**kwargs):
    """Create UrbanAccess accessibility network from the fake gtfs data

    The resulting network can then be loaded from Python code:

    import stride.urbanaccess.helpers;
    urbanaccess_net = stride.urbanaccess.helpers.load_network(network_path)

    See https://github.com/UDST/urbanaccess documentation for details on how to do analysis on this network.
    """
    from .create_network import main
    main(**kwargs)
