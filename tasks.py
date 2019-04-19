"""
Scrapper celery tasks
"""
import requests
from celery import Celery

import config
from libs import advert, page
from logmodule import get_logger

LOGGER = get_logger(__name__)

APP = Celery('tasks', broker=config.RABBIT_URL)


def put_ids_to_queue(ids_list):
    """
    Pushes list of advert ids to celery queue
    """
    LOGGER.debug('pushing %s ads to the queue', len(ids_list))
    for advert_id in ids_list:
        fetch_single_advert.delay(advert_id)


@APP.task(rate_limit='28/m', bind=True, default_retry_delay=60 * 60)
def fetch_single_advert(self, rid):
    """
    Fetching single advert
    """
    try:
        advert.fetch_advert(rid, persist=True)
    except requests.exceptions.HTTPError as exc:
        crawler_banned = exc.response.status_code == 403
        if crawler_banned:
            LOGGER.error('seems like we got banned (403), retrying in 1h')
            self.retry()
        LOGGER.error(exc)
    except AttributeError:
        LOGGER.error('Body parse error on %s', rid)


@APP.task(rate_limit='28/m', default_retry_delay=60 * 60)
def iterate_over_search_results(page_num=1):
    """
    Going through pagination results
    """
    LOGGER.info('fetching page %s', page_num)
    try:
        page_body = page.get_sresults_page(page_num)
    except requests.exceptions.HTTPError as exc:
        if exc.response.status_code == 403:
            # self.retry()
            return

    search_result_adverts = advert.extract_advert_ids_from_search_result_page(page_body)
    put_ids_to_queue(search_result_adverts)

    next_page, pages_count = page.get_sresults_pages_info(page_body)
    if next_page > pages_count:
        return

    iterate_over_search_results.delay(next_page)
