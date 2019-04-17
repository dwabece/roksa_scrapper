#!/usr/bin/env python3
"""
CLI interface for scrapper
"""
import json
from pprint import pprint as pp

import click
import requests

from libs import advert


@click.group()
def cli():
    """
    Click group initialization
    """


@cli.command()
@click.argument('rid')
@click.argument('persist')
def fetch(rid, persist_data):
    """
    Fetching and displaying ad by its id.

    Attributes:
        rid (rid): Advert id
    """
    try:
        res = advert.fetch_advert(rid, persist=persist_data, return_as_json=True)
    except requests.exceptions.HTTPError:
        raise SystemExit('Something went wrong, sorry mate')

    pp(json.loads(res))


if __name__ == '__main__':
    cli()
