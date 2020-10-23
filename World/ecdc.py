from config import settings
import requests
from common.helpers import trace_function
from collections import Counter
from common.helpers import to_date, week_number, trace_function
from World.corrections import CORRECTION_POLAND_05_10, CORRECTION_POLAND_06_10
from typing import Union
import pandas as pd
from functools import reduce

DATE_REP = "dateRep"
YEAR = "year"
MONTH = "month"
DAY = "day"
CASES = "cases"
DEATHS = "deaths"
TESTS_DONE = "tests_done"
HOSPITAL_RATE = "hospital_rate"
TESTS_DONE = "tests_done"
TESTING_RATE = "testing_rate"
POSITIVITY_RATE = "testing_positivity_rate"
TESTING_DATA_SOURCE = "testing_data_source"
COUNTRY = "country"
YEAR_WEEK = "year_week"


def __norm_year_week(yw):
    yw = yw.split("W")
    year = int(yw[0][0:4])
    week = yw[1]
    return f"{year}-W{int(week)}"  # remove leading zeros


@trace_function("Get cases")
def cases_by_country() -> list:
    cases = requests.get(url=settings.ECDC_CASE_DISTRIBUTION_URL)
    df = pd.DataFrame(cases.json().get("records", [])).rename(
        columns={"countriesAndTerritories": COUNTRY}
    )
    df.loc[(df[COUNTRY] == "United_States_of_America"), COUNTRY] = "United States"
    return df


@trace_function("Get testing")
def testing_by_country() -> list:
    testing = requests.get(url=settings.ECDC_COVID19_TESTING_URL)
    df = pd.DataFrame(testing.json()).rename(columns={"new_cases": CASES}).reset_index()
    df[YEAR_WEEK] = df[YEAR_WEEK].apply(__norm_year_week)
    return df


@trace_function("Get hospital rates")
def hospital_admission_rates() -> list:
    admission_rates = requests.get(url=settings.ECDC_HOSPITAL_ADMISSION_RATES_URL)
    df = pd.DataFrame(admission_rates.json()).rename(
        columns={
            "value": HOSPITAL_RATE,
            "source": "hospital_rate_source",
            "url": "hospital_rate_url",
        }
    )
    df[YEAR_WEEK] = df[YEAR_WEEK].apply(__norm_year_week)
    return df


@trace_function("Combine data sets and aggregate weekly ")
def weekly(
    cases: pd.DataFrame,
    testing: pd.DataFrame = None,
    hospital_rates: pd.DataFrame = None,
) -> pd.DataFrame:
    """Combine provided data sets and aggregate statistics weekly"""
    cases[YEAR_WEEK] = cases.apply(
        lambda row: f"{row['year']}-W{week_number(to_date(row))}", axis=1
    )
    df_final = (
        cases.groupby([COUNTRY, YEAR_WEEK])[[CASES, DEATHS]].agg("sum").reset_index()
    )

    if testing is not None:
        testing_data = testing.set_index([COUNTRY, YEAR_WEEK])
        cols_to_use = testing.columns.difference(df_final.columns)
        df_final = pd.merge(
            df_final, testing_data[cols_to_use], on=[COUNTRY, YEAR_WEEK], how="outer"
        ).set_index([COUNTRY, YEAR_WEEK])

    if hospital_rates is not None:
        hospital_data = hospital_rates.groupby([COUNTRY, YEAR_WEEK])[
            [HOSPITAL_RATE]
        ].agg(
            "sum"
        )  # some countries have daily data for hospital rate
        cols_to_use = hospital_data.columns.difference(df_final.columns)
        df_final = pd.merge(
            df_final, hospital_data[cols_to_use], on=[COUNTRY, YEAR_WEEK], how="outer"
        )

    return df_final.reset_index()
