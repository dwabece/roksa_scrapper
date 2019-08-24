"""
Logic responsible for parsing and extracting vital data
from ad's HTML body
"""
import json

from bs4 import BeautifulSoup
# from pymongo import MongoClient

from libs.page import get_advert_page
from logmodule import get_logger
from libs import utils

# Mongo initialization
# MONGO_CLIENT = MongoClient(config.get_mongo_url())
# DB = MONGO_CLIENT.get_database(config.MONGO.get('db'))
# ADVERT_COL = DB.get_collection('advert')


LOGGER = get_logger(__name__)


def fetch_advert(roksa_id, persist=False, return_as_json=False):
    """
    Parameters:
        roksa_id (int): advert id from portal
        persist (bool): tells wether save result into mongo or not
        return_as_json (bool): tells wether return JSON serialized object
            or python dictionary

    Returns:
        dict|string: advert parameters, as dict or JSON serialized,
            depends on `return_as_json` argument
    """
    # @TODO tryexcept that
    www_body = get_advert_page(roksa_id)

    page_data = _parse_ad(www_body)

    # if persist:
    #   _persist_advert(page_data)

    if return_as_json:
        return json.dumps(page_data)

    return page_data


# def _persist_advert(advert_data, check_if_exists=True):
#     """
#     Saves fetched advert data to mongo collection

#     Parameters:
#         advert_data (dict): dict containing set of found ad attributes
#         check_if_exists (bool): verify if such ad already exists
#             before inserting it

#     Returns:
#         object: pymongo element object
#     """
#     if check_if_exists:
#         existing = ADVERT_COL.find_one({'id': advert_data['id']})
#         if existing:
#             return existing.get('_id')
#     res = ADVERT_COL.insert(advert_data)

#     return res

def _load_page_body(html):
    return BeautifulSoup(html, 'html.parser')


def _parse_ad(page_body):
    """
    Loads page source, parses it then extracts and returns advert attributes.

    Parameters:
        page_body (str): html source of fetched advert page

    Returns:
        dict: advert attributes with their values
    """
    soup = _load_page_body(page_body)

    fields_to_fetch = {
        'rid': _get_ad_id,
        'name': _get_ad_name,
        'services': _get_services,
        'description': _get_ad_description,
    }

    result = {}

    for field, fn in fields_to_fetch.items():
        try:
            result.update({
                field: fn(soup)
            })
        except AttributeError as exc:
            LOGGER.debug(exc)
            raise

    commonfields = _get_commonfields(soup)
    result.update(commonfields)

    return result


def _get_ad_id(soup_body):
    """
    Helper function that extracts and returns advert id from page body

        Returns:
        dict: dict containing `id` key and list of services
            passed as a python list
    """
    value = (
        soup_body.find('head')
        .find('link', {'rel': 'canonical'}, href=True)
        .get('href', 'Not found')
    )
    return value.split('/')[-1]
    # return {'id': value.split('/')[-1]}


def _get_ad_name(soup_body):
    """
    Helper function that fetches Diva's nickname from page body

        Returns:
        dict: dict containing `name` key and list of services
    """
    return (
        soup_body.find('div', attrs={'id': 'anons_header'})
        .find('h2')
        .get_text()
        .strip()
    )


def _get_ad_description(soup_body):
    """
    Helper function that fetches Diva's advert description from page

        Returns:
        dict: dict containing `description` key and description text
    """
    desc_container = soup_body.find('div', attrs={'id': 'anons_content'}).find(
        'div', attrs={'id': 'tresc_pl'}
    )

    return ' '.join(desc_container.stripped_strings)


def _get_services(soup_body):
    """
    Returns services being provided by Escort as a list

    Returns:
        dict: dict containing `tags` key and list of provided services
    """
    tags_soup = soup_body.find_all('p', attrs={'class': 'tag'})
    tags_list = [tag.get_text(strip=True).lower() for tag in tags_soup]

    return tags_list


def _get_commonfields(soup_body):
    """
    Fetches ad details that are listed in the page's left column
    eg. height, weight, breast size and prices

    Returns:
        dict: advert attributes with their values

    """
    def sanitize_value(value):
        return value.lower().strip()

    def parse_unitary_value(value):
        return value.split()[0]

    def parse_list_value(value):
        if value == '-':
            return []

        return value.split()

    def parse_phone(value):
        return value.replace(' ', '').replace('+', '').replace('48', '').replace('-', '')

    ad_attributes_list = soup_body.find('div', attrs={'id': 'anons_details'}).find('ul').find_all('li')

    fields_mapping = {
        'phone_number': parse_phone,
        'city': None,
        'district': None,
        'out_calls': None,
        'age': None,
        'weight': parse_unitary_value,
        'height': parse_unitary_value,
        'breast': parse_unitary_value,
        'languages': parse_list_value,
        '1_hour': parse_unitary_value,
        '15_min': parse_unitary_value,
        '30_min': parse_unitary_value,
        'all_night': parse_unitary_value,
    }

    remap_field_names = {
        '1_hour': 'price_hour',
        '15_min': 'price_quarter',
        '30_min': 'price_half',
        'all_night': 'price_night',
    }

    commonfields_ = {}

    for item in ad_attributes_list:
        # each `data row` is made out of two spans
        # fist one contains key, second one value of an attribute
        kv = item.find_all('span')

        field_name = utils.slugify(kv[0].text)
        if field_name not in fields_mapping.keys():
            continue

        value = sanitize_value(kv[1].text)
        fn = fields_mapping[field_name]
        if fn:
            value = fn(value)

        # renaming field name
        field_name = remap_field_names.get(field_name) or field_name
        commonfields_[field_name] = value

    return commonfields_


def extract_advert_ids_from_search_result_page(page_body):
    """
    Extracts adverts from page html
    """
    body_container = BeautifulSoup(page_body, 'html.parser')
    adverts_container = body_container.find(id='anons_group')
    ads = adverts_container.find_all('a')

    return [int(a['href'].split('/')[-1]) for a in ads]
