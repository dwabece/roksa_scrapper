import json
from celery import Celery
import requests
import config
from logmodule import get_logger
from libs import advert

logger = get_logger(__name__)

app = Celery(
    'tasks',
    broker=config.RABBIT_URL
)


def put_ids_to_queue(ids_list):
    logger.debug(f'pushing {len(ids_list)} ads to the queue')
    for advert_id in ids_list:
        fetch_single_advert.delay(advert_id)


@app.task(rate_limit='50/m', bind=True, default_retry_delay=60 * 60)
def fetch_single_advert(self, rid):
    """
    Task that fetches advert
    """
    try:
        logger.info(f'fetching: {rid}')
        result = advert.fetch_advert(rid, persist=True)
        logger.debug(result)
    except requests.exceptions.HTTPError as e:
        crawler_banned = e.response.status_code == 403
        if crawler_banned:
            logger.error('seems like we got banned (403), retrying in 1h')
            self.retry()
        logger.error(e)
    except AttributeError:
        logger.error(f'Body parse error on {rid}')
    except Exception as e:
        logger.error(e)
        pass
