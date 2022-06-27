import json

import click


@click.group(context_settings={'max_content_width': 200})
def main():
    """Open Bus Stride Client"""
    pass


from .urbanaccess.cli import urbanaccess
main.add_command(urbanaccess)


@main.command()
@click.argument('PATH')
@click.argument('PARAMS_JSON', default='{}')
@click.option('--use-proxy-server', is_flag=True)
def get(path, params_json, use_proxy_server):
    """Get a single API path with optional json params and print the result"""
    from . import common, api_proxy
    with api_proxy.start(use_proxy_server):
        print(common.get(path, json.loads(params_json)))


@main.command()
@click.argument('PATH')
@click.argument('PARAMS_JSON', default='{}')
@click.option('--limit', default=1000)
@click.option('--use-proxy-server', is_flag=True)
def iterate(path, params_json, limit, use_proxy_server):
    """Iterate over an API list path with optional json params, print one item per line"""
    from . import streaming, api_proxy
    i = -1
    with api_proxy.start(use_proxy_server):
        for i, item in enumerate(streaming.iterate(path, json.loads(params_json), limit)):
            print(item)
    print(f"Got {i+1} results")


if __name__ == "__main__":
    main()
