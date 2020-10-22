
from numpy.lib.arraysetops import unique
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import common.helpers as helpers
import pandas as pd
import World.ecdc as ecdc
import numpy as np

MODE_LINES_N_MARKERS = "lines+markers"


@helpers.trace_function("Case distribution multi-graph")
def case_distribution_subplots(df: pd.DataFrame, title: str) -> go.Figure:
    countries = df[ecdc.COUNTRY].unique()
    N = len(countries)

    fig = make_subplots(
        rows=N,
        cols=1,
        subplot_titles=countries,
        shared_xaxes=True,
        vertical_spacing=0.05,
    )
    
    def sort_func(row):
        yw = row[ecdc.YEAR_WEEK].split('-W')
        week = yw[1]
        return int(week)

    for n in range(0, N):
        c = countries[n]
        sub_df = df.loc[df[ecdc.COUNTRY] == c]

        seq_col = sub_df.apply(sort_func, axis=1)
        sub_df = sub_df.assign(seq=seq_col.values).sort_values('seq')

        fig.add_trace(
            go.Scatter(
                x=sub_df[ecdc.YEAR_WEEK],
                y=sub_df[ecdc.HOSPITAL_RATE],
                mode=MODE_LINES_N_MARKERS,
                name=f'{c} {ecdc.HOSPITAL_RATE.replace("_", " ")}',
            ),
            row=n + 1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=sub_df[ecdc.YEAR_WEEK],
                y=sub_df[ecdc.DEATHS],
                mode=MODE_LINES_N_MARKERS,
                name=f'{c} {ecdc.DEATHS.replace("_", " ")}',
            ),
            row=n + 1,
            col=1,
        )
        
        fig.add_trace(
            go.Bar(
                x=sub_df[ecdc.YEAR_WEEK],
                y=sub_df[ecdc.CASES],
                name=f'{c} {ecdc.CASES.replace("_", " ")}',
            ),
            row=n + 1,
            col=1,
        )

    fig.update_layout(height=1200, width=1000, title_text=title)
    return fig
