import World.ecdc as ecdc
import mock
from config import settings
import json


def cases_by_country_mock_data() -> dict:
    with open("./tests/ecdc_cases.json") as file:
        return json.load(file)


def testing_by_country_mock_data() -> dict:
    with open("./tests/ecdc_testing.json") as file:
        return json.load(file)


def hospital_admission_rates_mock_data() -> dict:
    with open("./tests/ecdc_hospital_rates.json") as file:
        return json.load(file)


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs["url"] == settings.ECDC_CASE_DISTRIBUTION_URL:
        return MockResponse(cases_by_country_mock_data(), 200)
    if kwargs["url"] == settings.ECDC_COVID19_TESTING_URL:
        return MockResponse(testing_by_country_mock_data(), 200)
    if kwargs["url"] == settings.ECDC_HOSPITAL_ADMISSION_RATES_URL:
        return MockResponse(hospital_admission_rates_mock_data(), 200)
    return MockResponse(None, 404)


@mock.patch("requests.get", mocked_requests_get)
def test_cases_by_country():
    df = ecdc.cases_by_country()
    # test sample data from dataset
    countries = [
        "Poland",
        "Germany",
        "Czechia",
        "Slovakia",
        "Ukraine",
        "Belarus",
        "Lithuania",
        "Russia",
    ]
    assert df.loc[df[ecdc.COUNTRY].isin(countries)].bool


@mock.patch("requests.get", mocked_requests_get)
def test_testing_by_country():
    df = ecdc.testing_by_country()
    pl_df = df.loc[df[ecdc.COUNTRY] == "Poland"]
    # test sample data from dataset
    pl_W10 = pl_df.loc[pl_df[ecdc.YEAR_WEEK] == "2020-W10"]
    tests_done = pl_W10[ecdc.TESTS_DONE].values
    assert tests_done == 603


@mock.patch("requests.get", mocked_requests_get)
def test_hospital_admission_rates():
    df = ecdc.hospital_admission_rates()
    pl_df = df.loc[df[ecdc.COUNTRY] == "Poland"]
    # test sample data from dataset
    pl_W15 = pl_df.loc[pl_df[ecdc.YEAR_WEEK] == "2020-W15"]
    hospital_rate = pl_W15[ecdc.HOSPITAL_RATE].values
    assert hospital_rate == 2425
