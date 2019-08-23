"""
Logic responsible for parsing and extracting vital data
from ad's HTML body
"""
import json

from bs4 import BeautifulSoup
# from pymongo import MongoClient

import config
from libs.page import get_advert_page
from logmodule import get_logger

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
        # _persist_advert(page_data)

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
        'id': _get_ad_name,
        # _get_ad_id,
        # _get_services,
        # _get_ad_description,
        # _get_commonfields,
    }

    result = {}

    for field_function in fields_to_fetch:
        try:
            result.update(field_function(soup))
        except AttributeError as exc:
            LOGGER.debug(exc)
            raise

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
    # return {'name': value}


def _get_ad_description(soup_body):
    """
    Helper function that fetches Diva's advert description from page

        Returns:
        dict: dict containing `description` key and description text
    """
    desc_container = soup_body.find('div', attrs={'id': 'anons_content'}).find(
        'div', attrs={'id': 'tresc_pl'}
    )
    return {'description': desc_container.get_text(strip=True)}


def _get_services(soup_body):
    """
    Returns services being provided by Escort as a list

    Returns:
        dict: dict containing `tags` key and list of provided services
    """
    tags_soup = soup_body.find_all('p', attrs={'class': 'tag'})
    tags_list = [tag.get_text(strip=True).lower() for tag in tags_soup]

    return {'tags': tags_list}


def _get_commonfields(soup_body):
    """
    Fetches ad details that are listed in the page's left column
    eg. height, weight, breast size and prices

    Returns:
        dict: advert attributes with their values
    """
    result = {}

    def sanitize_attribute_key(txt_val):
        return txt_val.lower().split(':')[0]

    ad_attributes_list = (
        soup_body.find('div', attrs={'id': 'anons_details'}).find('ul').find_all('li')
    )

    desired_fields = (
        'phone number',
        'city',
        'district',
        'age',
        'weight',
        'height',
        'breast',
        'languages',
        '1 hour',
    )

    fields_values_mapping = {
        'weight': _parse_commonfields_numeric,
        'height': _parse_commonfields_numeric,
        'languages': _parse_commonfields_list,
        '1 hour': _parse_commonfields_numeric,
    }

    for item in ad_attributes_list:
        obj_attr_label = item.find('span')
        obj_attr_value = obj_attr_label.find_next_sibling()

        attr_name = sanitize_attribute_key(obj_attr_label.get_text(strip=True))

        if attr_name not in desired_fields or not obj_attr_value:
            continue

        attr_value = obj_attr_value.get_text(strip=True)

        value_map_fn = fields_values_mapping.get(attr_name)
        if value_map_fn:
            attr_value = value_map_fn(attr_value)

        result[attr_name] = attr_value

    return result


def _parse_commonfields_numeric(txt_val):
    """
    Helper function to remove unneccessary unit from numeric fields
    """
    return int(txt_val.split()[0])


def _parse_commonfields_list(txt_val):
    """
    Helper function that splits coma separated elements to list
    """
    return list({item.strip() for item in txt_val.split(',') if item})


def extract_advert_ids_from_search_result_page(page_body):
    """
    Extracts adverts from page html
    """
    body_container = BeautifulSoup(page_body, 'html.parser')
    adverts_container = body_container.find(id='anons_group')
    ads = adverts_container.find_all('a')

    return [int(a['href'].split('/')[-1]) for a in ads]
