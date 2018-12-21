"""
Logic responsible for parsing and extracting vital data
from ad's HTML body
"""
from bs4 import BeautifulSoup


def parse_ad(page_body):
    """
    Loads page source, parses it then extracts and returns advert attributes.

    Parameters:
        page_body (str): html source of fetched advert page

    Returns:
        dict: advert attributes with their values
    """
    fields_to_parse = (_get_ad_name, _get_ad_id, _get_services,
                       _get_ad_description, _get_commonfields)

    soup = BeautifulSoup(page_body, 'html.parser')
    result = {}

    for field_fnc in fields_to_parse:
        try:
            result.update(field_fnc(soup))
        except Exception as exc:
            print(type(exc), exc)

    return result


def _get_ad_id(soup_body):
    """
    Helper function that extracts and returns advert id from page body

        Returns:
        dict: dict containing `id` key and list of services
            passed as a python list
    """
    value = soup_body.find('head').find('link', {'rel': 'canonical'}, href=True).get('href', 'Not found')
    return {'id': value.split('/')[-1]}


def _get_ad_name(soup_body):
    """
    Helper function that fetches Diva's nickname from page body

        Returns:
        dict: dict containing `name` key and list of services
    """
    value = soup_body.find('div', attrs={'id': 'anons_header'}).find('h2').get_text().strip()
    return {'name': value}


def _get_ad_description(soup_body):
    """
    Helper function that fetches Diva's advert description from page

        Returns:
        dict: dict containing `description` key and description text
    """
    desc_container = soup_body.find('div', attrs={'id': 'anons_content'})\
        .find('div', attrs={'id': 'tresc_pl'})
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

    ad_attributes_list = soup_body.find('div', attrs={'id': 'anons_details'})\
        .find('ul').find_all('li')

    desired_fields = {
        'phone number': None,
        'city': None,
        'district': None,
        'age': None,
        'weight': _parse_commonfields_numeric,
        'height': _parse_commonfields_numeric,
        'breast': None,
        'languages': _parse_commonfields_list,
        '1 hour': _parse_commonfields_numeric,
    }

    for item in ad_attributes_list:
        obj_attr_label = item.find('span')
        obj_attr_value = obj_attr_label.find_next_sibling()
        attr_name = sanitize_attribute_key(obj_attr_label.get_text(strip=True))

        if attr_name in desired_fields and obj_attr_value:
            attr_value_text = obj_attr_value.get_text(strip=True)
            value_parse_fn = desired_fields[attr_name]

            result[attr_name] = value_parse_fn(attr_value_text) if value_parse_fn else attr_value_text

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
    return [item.strip() for item in txt_val.split(',') if item]
