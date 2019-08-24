import re
import unicodedata
from dataclasses import dataclass


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '_', value)


@dataclass
class Advert:
    rid: str
    name: str
    services: list
    description: str
    phone_number: str
    city: str
    district: str
    out_calls: str
    age: int
    weight: int
    height: int
    breast: int
    languages: list
    price_hour: int
    price_quarter: int
    price_half: int
    price_night: int
