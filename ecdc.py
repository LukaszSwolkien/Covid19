from config import settings
import requests
from helpers import trace_function

# TODO: map ECDC schema to internal schema in all functions

@trace_function("Get cases")
def cases_by_country() -> list:
    cases = requests.get(url=settings.ECDC_CASE_DISTRIBUTION_URL)
    return cases.json().get("records", [])


@trace_function("Get testing")
def testing_by_country_weekly() -> list:
    testing = requests.get(url=settings.ECDC_COVID19_TESTING_URL)
    return testing.json()


@trace_function("Get hospital rates")
def hospitel_admission_rates_weekly() -> list:
    admission_rates = requests.get(url=settings.ECDC_HOSPITAL_ADMISSION_RATES_URL)
    return admission_rates.json()
