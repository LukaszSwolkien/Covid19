from config import settings
import requests


def cases_by_country() -> list:
    # with tracer.start_as_current_span('Get all available open data'):
    cases = requests.get(url=settings.ECDC_CASE_DISTRIBUTION_URL)
    return cases.json().get("records", [])


def testing_by_country_weekly() -> list:
    testing = requests.get(url=settings.ECDC_COVID19_TESTING_URL)
    return testing.json()


def hospitel_admission_rates_weekly() -> list:
    admission_rates = requests.get(url=settings.ECDC_HOSPITAL_ADMISSION_RATES_URL)
    return admission_rates.json()
