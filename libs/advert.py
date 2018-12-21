"""
Logic responsible for parsing and extracting vital data
from ad's HTML body
"""
from bs4 import BeautifulSoup


def parse_ad(page_body):
    ad_fields_list = (_get_ad_name, _get_ad_id)
    soup = BeautifulSoup(page_body, 'html.parser')
    result = {}

    for field_fnc in ad_fields_list:
        try:
            result.update(field_fnc(soup))
        except Exception as e:
            print(type(e), e)
            pass

    return result


def _get_ad_name(soup_body):
    value = soup_body.find('div', attrs={'id': 'anons_header'}).find('h2').get_text().strip()
    return {'name': value}


def _get_ad_id(soup_body):
    value = soup_body.find('head').find('link', {'rel': 'canonical'}, href=True).get('href', 'Not found')
    return {'id': value.split('/')[-1]}
