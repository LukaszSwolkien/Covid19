
from config import settings
import requests


def cases_by_country() -> list:
    URL = settings.CASE_DISTRIBUTION_URL

    r = requests.get(url=URL)
    data = r.json()
    return data['records']