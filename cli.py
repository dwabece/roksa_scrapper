#!/usr/bin/env python
import sys
from libs import page


def run():
    try:
        rid = int(sys.argv[1])
    except IndexError:
        rid = 602586  # ;)

    print(page.fetch_advert_data(rid))


if __name__ == '__main__':
    run()
