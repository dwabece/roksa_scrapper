#!/usr/bin/env python
import sys
from libs.advert import fetch_advert
import libs.page as page


def run():
    # try:
    #     rid = int(sys.argv[1])
    # except IndexError:
    #     rid = 602586  # ;)

    # print(fetch_advert(rid, False))
    page.paginate_search_results()


if __name__ == '__main__':
    run()
