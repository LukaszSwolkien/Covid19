"""
Country data
"""
import json
from config import settings
from common.helpers import trace_function

@trace_function('Load countries static data from file')
def load_countries_data() -> dict:
    countries_data = {}
    with open(f'./World/{settings.COUNTRIES_DATA_FILE}') as file:
        data = json.load(file)
        for i in data:
            countries_data[i['country']] = i['population']
    return countries_data
