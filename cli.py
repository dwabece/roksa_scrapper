#!/usr/bin/env python
import sys
from libs.advert import fetch_advert


def run():
    try:
        rid = int(sys.argv[1])
    except IndexError:
        rid = 602586  # ;)

    print(fetch_advert(rid, True))


if __name__ == '__main__':
    run()
