import Poland.poland_stats as stats
from config import settings
import mock
import json
import pandas as pd


def test_covid_19_timeline():
    df_his = pd.read_json("./tests/poland_stats.json")

    df_latest = stats.covid_19_timeline()

    df_h = df_his.loc[df_his[stats.DATE] == "22/10/2020"]
    active_h = df_h[stats.ACTIVE].values
    assert active_h == 108463

    df_l = df_latest.loc[df_latest[stats.DATE] == "22/10/2020"]
    active_l = df_l[stats.ACTIVE].values
    assert active_h == active_l
