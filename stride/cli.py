import json

import click


@click.group(context_settings={'max_content_width': 200})
def main():
    """Open Bus Stride Client"""
    pass


@main.command()
@click.argument('PATH')
@click.argument('PARAMS_JSON', default='{}')
def get(path, params_json):
    """Get a single API path with optional json params and print the result"""
    from . import common
    print(common.get(path, json.loads(params_json)))


@main.command()
@click.argument('PATH')
@click.argument('PARAMS_JSON', default='{}')
@click.option('--limit', default=1000)
def iterate(path, params_json, limit):
    """Iterate over an API list path with optional json params, print one item per line"""
    from . import streaming
    for i, item in enumerate(streaming.iterate(path, json.loads(params_json), limit)):
        print(item)
    print(f"Got {i+1} results")


if __name__ == "__main__":
    main()
