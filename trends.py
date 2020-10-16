from collections import Counter
from helpers import to_date, week_number, trace_function
from corrections import CORRECTION_POLAND_05_10, CORRECTION_POLAND_06_10


def __select_and_sort(data, country):
    selector = lambda x: (x["countriesAndTerritories"] == country)
    selected_data = list(filter(selector, data))
    return sorted(
        selected_data, key=lambda x: (int(x["year"]), int(x["month"]), int(x["day"]))
    )


def __aggregate(f, data):
    agg_data = dict()
    z_stats = {"cases": 0, "deaths": 0}
    for v in data:
        ym = f(v)
        curr = agg_data.get(ym, z_stats)
        summary = Counter(curr) + Counter({"cases": v["cases"], "deaths": v["deaths"]})
        agg_data[ym] = summary
    return agg_data


def __trends_schema(data):
    return [
        {
            "dateRep": k,
            "year": v["year"],
            "month": v["month"],
            "day": v["day"],
            "cases": v["cases"],
            "deaths": v["deaths"],
            "tests_done": v.get("testing", {}).get("tests_done", None),
            "hospital_rate": v.get("hospital", {}).get("value", None),
        }
        for k, v in data.items()
    ]


@trace_function("Aggregate monthly data")
def monthly(data: list, country: str) -> list:
    selector = lambda x: x["countriesAndTerritories"] == country
    selected_data = list(filter(selector, data))
    sorted_selected_data = sorted(
        selected_data, key=lambda x: (int(x["month"]), int(x["day"]))
    )

    agg_data = __aggregate(lambda v: f'{v["month"]}/{v["year"]}', sorted_selected_data)

    return __trends_schema(agg_data)


@trace_function("Curate data for daily load")
def daily(cases: list, country: str) -> list:
    sorted_selected_data = __select_and_sort(cases, country)

    def correct_fun(x):
        if country != "Poland":
            return x
        if x["dateRep"] == "05/10/2020":
            return CORRECTION_POLAND_05_10
        elif x["dateRep"] == "06/10/2020":
            return CORRECTION_POLAND_06_10
        return x

    return list(map(correct_fun, sorted_selected_data))


@trace_function("Combine and aggregate weekly data")
def weekly(
    cases: list, country: str, testing: list = [], hospital_rates: list = []
) -> list:
    sorted_selected_data = __select_and_sort(cases, country)

    weekly_cases = __aggregate(
        lambda v: f'{v["year"]}-W{week_number(to_date(v))}', sorted_selected_data
    )

    for td in testing:
        if td["country"] == country and td["year_week"] in weekly_cases:
            weekly_cases[td["year_week"]]["testing"] = {
                "new_cases": td.get("new_cases"),
                "tests_done": td.get("tests_done"),
                "population": td.get("population"),
                "testing_rate": td.get("testing_rate"),
                "positivity_rate": td.get("positivity_rate"),
                "testing_data_source": td.get("testing_data_source", ""),
            }
    for hr in hospital_rates:
        if hr["country"] == country and hr["year_week"] in weekly_cases:
            weekly_cases[hr["year_week"]]["hospital"] = {
                "value": hr.get("value"),
                "source": hr.get("source", ""),
                "url": hr.get("url", ""),
            }

    return __trends_schema(weekly_cases)
