import json
from celery import Celery
import requests
import config
from logmodule import get_logger
from libs import advert, page

logger = get_logger(__name__)

app = Celery(
    'tasks',
    broker=config.RABBIT_URL
)


def put_ids_to_queue(ids_list):
    logger.debug(f'pushing {len(ids_list)} ads to the queue')
    for advert_id in ids_list:
        fetch_single_advert.delay(advert_id)


@app.task(rate_limit='28/m', bind=True, default_retry_delay=60 * 60)
def fetch_single_advert(self, rid):
    """
    Fetching single advert
    """
    try:
        advert.fetch_advert(rid, persist=True)
    except requests.exceptions.HTTPError as e:
        crawler_banned = e.response.status_code == 403
        if crawler_banned:
            logger.error('seems like we got banned (403), retrying in 1h')
            self.retry()
        logger.error(e)
    except AttributeError:
        logger.error('Body parse error on %s', rid)


@app.task(rate_limit='28/m', default_retry_delay=60 * 60)
def iterate_over_search_results(page_num=1):
    """
    Going through pagination results
    """
    logger.info('fetching page %s', page_num)
    try:
        page_body = page.get_sresults_page(page_num)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            # self.retry()
            return

    search_result_adverts = advert.extract_advert_ids_from_search_result_page(page_body)
    put_ids_to_queue(search_result_adverts)

    next_page, pages_count = page.get_sresults_pages_info(page_body)
    print(next_page, pages_count)
    if next_page > pages_count:
        return

    iterate_over_search_results.delay(next_page)
