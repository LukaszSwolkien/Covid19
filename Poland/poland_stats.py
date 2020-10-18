import pandas as pd
import datetime
import common.helpers as helpers
from config import settings


pd.options.plotting.backend = "plotly"

QUARANTINED = "Quarantined"
MONITORED = "Monitored"
TESTED_TOTAL = "Tested total"
CONFIRMED_DAILY = "Confirmed daily"
CONFIRMED = "Confirmed"
ACTIVE = "Active"
RECOVERED = "Recovered"
DEATHS_DAILY = "Deaths daily"


@helpers.trace_function('Get Poland covid-19 timeline stats')
def covid_19_timeline():
    dfs = pd.read_html(settings.WIKIPEDIA_POLAND_STATS_URL)
    df = dfs[2]
    df.rename(
        columns={
            "Date (CET)": "Date",
            "Quarantined[a]": QUARANTINED,
            "Tested (total)[b]": TESTED_TOTAL,
            "Confirmed daily[c]": CONFIRMED_DAILY,
            "Recovered[d]": RECOVERED,
            "Official deaths daily[e]": DEATHS_DAILY,
        },
        inplace=True,
    )

    del df["Unofficial deaths daily[f]"]
    del df["Source(s)[g]"]

    date_format = "%d %B %Y"  # ex.: 30 September 2020

    def correct_date(date_text):
        try:
            date_datetime = datetime.datetime.strptime(date_text, date_format)
        except ValueError:
            s = date_text.split("[")
            if len(s) > 1:
                date_text = s[0]
                return correct_date(date_text)
            return "invalid"
        return date_datetime.strftime("%d/%m/%Y")

    df["Date"] = df["Date"].apply(correct_date)
    df = df[df["Date"] != "invalid"]
    df = df.set_index(pd.DatetimeIndex(df["Date"]))

    def format_number(x):
        if isinstance(x, str):
            if helpers.is_num(x):
                x = x.replace(",", "")
                return int(x)
            else:
                return None
        return x

    df[QUARANTINED] = df[QUARANTINED].apply(format_number)
    df[MONITORED] = df[MONITORED].apply(format_number)
    df[TESTED_TOTAL] = df[TESTED_TOTAL].apply(format_number)
    df[CONFIRMED_DAILY] = df[CONFIRMED_DAILY].apply(format_number)
    df[CONFIRMED] = df[CONFIRMED].apply(format_number)
    df[ACTIVE] = df[ACTIVE].apply(format_number)
    df[RECOVERED] = df[RECOVERED].apply(format_number)
    df[DEATHS_DAILY] = df[DEATHS_DAILY].apply(format_number)

    return df
