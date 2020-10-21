from config import settings
import requests
from common.helpers import trace_function
from collections import Counter
from common.helpers import to_date, week_number, trace_function
from World.corrections import CORRECTION_POLAND_05_10, CORRECTION_POLAND_06_10
from typing import Union

DATE_REP = "dateRep"
YEAR = "year"
MONTH = "month"
DAY = "day"
CASES = "cases"
DEATHS = "deaths"
TESTS_DONE = "tests_done"
HOSPITAL_RATE = "hospital_rate"
NEW_CASES = "new_cases"
TESTS_DONE = "tests_done"
TESTING_RATE = "testing_rate"
POSITIVITY_RATE = "positivity_rate"
TESTING_DATA_SOURCE = "testing_data_source"
COUNTRY = 'country'


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


def __select_and_sort(data, country):
    selector = lambda x: (x["countriesAndTerritories"] == country)
    selected_data = list(filter(selector, data))
    return sorted(
        selected_data, key=lambda x: (int(x[YEAR]), int(x[MONTH]), int(x[DAY]))
    )


def __aggregate(f, data):
    agg_data = dict()
    z_stats = {CASES: 0, DEATHS: 0}
    for v in data:
        ym = f(v)
        curr = agg_data.get(ym, z_stats)
        summary = Counter(curr) + Counter({CASES: v["cases"], DEATHS: v["deaths"]})
        agg_data[ym] = summary
    return agg_data

def __timeline_dict(data):
    res = {}

    for d in data:
        e = [{
                DATE_REP: k,
                CASES: v.get("cases", 0),
                DEATHS: v.get("deaths", 0),
                TESTS_DONE: v.get("testing", {}).get("tests_done", None),
                HOSPITAL_RATE: v.get("hospital", {}).get("value", None),
            } for k, v in data[d].items()]
        res[d] = e
    return res


def __timeline_list(data):
    res = []

    for d in data:
        e = [{
                DATE_REP: k,
                CASES: v.get("cases", 0),
                COUNTRY: d,
                DEATHS: v.get("deaths", 0),
                TESTS_DONE: v.get("testing", {}).get("tests_done", None),
                HOSPITAL_RATE: v.get("hospital", {}).get("value", None),
            } for k, v in data[d].items()]
        res += e
    return res


@trace_function("Curate data for daily load")
def daily(cases: list, country: str) -> list:
    sorted_selected_data = __select_and_sort(cases, country)

    def correct_fun(x):
        if country != "Poland": # we know data correction only for Poland, but this function may need to be extended to other countries too.
            return x
        if x[DATE_REP] == "05/10/2020":
            return CORRECTION_POLAND_05_10
        elif x[DATE_REP] == "06/10/2020":
            return CORRECTION_POLAND_06_10
        return x

    return list(map(correct_fun, sorted_selected_data))

# TODO - refactor to pd.DataFrame and simplify this code.
@trace_function("Combine and aggregate weekly data")
def weekly(
    cases: list, country: str, testing: list = [], hospital_rates: list = []
) -> list:
    """Data aggregated weekly

    """
    sorted_selected_data = __select_and_sort(cases, country)
    weekly_cases = {}
    weekly_cases[country] = __aggregate(
        lambda v: f'{v[YEAR]}-W{week_number(to_date(v))}', sorted_selected_data
    )

    for td in testing:
        if td["country"] == country and td["year_week"] in weekly_cases:
            weekly_cases[td["year_week"]]["testing"] = {
                NEW_CASES: td.get("new_cases"),
                TESTS_DONE: td.get("tests_done"),
                TESTING_RATE: td.get("testing_rate"),
                POSITIVITY_RATE: td.get("positivity_rate"),
                TESTING_DATA_SOURCE: td.get("testing_data_source", ""),
            }
    for hr in hospital_rates:
        if hr["country"] == country and hr["year_week"] in weekly_cases:
            weekly_cases[hr["year_week"]]["hospital"] = {
                "value": hr.get("value"),
                "source": hr.get("source", ""),
                "url": hr.get("url", ""),
            }

    return __timeline_list(weekly_cases)

# TODO - refactor to pd.DataFrame and simplify this code.
@trace_function("Combine and aggregate weekly data")
def weekly_all_countries(
    cases: list, testing: list = [], hospital_rates: list = [], flatten=True,
) -> Union[list,dict]:
    """Data aggregated weekly

    """
    weekly_cases = {}
    countries = list(set(dic['countriesAndTerritories'] for dic in cases)) 
    for country in countries:
        sorted_selected_data = __select_and_sort(cases, country)

        weekly_cases[country] = __aggregate(
            lambda v: f'{v[YEAR]}-W{week_number(to_date(v))}', sorted_selected_data
        )

        for td in testing:
            if td["country"] == country and td["year_week"] in weekly_cases[country].keys():
                weekly_cases[country][td["year_week"]]["testing"] = {
                    NEW_CASES: td.get("new_cases"),
                    TESTS_DONE: td.get("tests_done"),
                    TESTING_RATE: td.get("testing_rate"),
                    POSITIVITY_RATE: td.get("positivity_rate"),
                    TESTING_DATA_SOURCE: td.get("testing_data_source", ""),
                }
        for hr in hospital_rates:
            if hr["country"] == country and hr["year_week"] in weekly_cases[country].keys():
                weekly_cases[country][hr["year_week"]]["hospital"] = {
                    "value": hr.get("value"),
                    "source": hr.get("source", ""),
                    "url": hr.get("url", ""),
                }

    return __timeline_list(weekly_cases) if flatten else __timeline_dict(weekly_cases)



