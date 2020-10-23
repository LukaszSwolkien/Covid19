import plotly.graph_objects as go
import common.helpers as helpers
from Poland.poland_stats import (
    DATE,
    QUARANTINED,
    CONFIRMED_DAILY,
    DEATHS_DAILY,
    ACTIVE,
    RECOVERED,
)

MODE_LINES_N_MARKERS = "lines+markers"

ACTIVE_PERCENTAGE = "Active percentage"
QUARANTINED_PERCENTAGE = "Quarantined percentage"


@helpers.trace_function("Active cases percentage graph")
def active_percentage(df, days_no, title):
    fig = go.Figure()

    fig.add_traces(
        go.Bar(
            x=df[DATE][-days_no:],
            y=df[ACTIVE_PERCENTAGE][-days_no:],
            name=ACTIVE_PERCENTAGE,
        )
    )
    fig.update_layout(
        title=title,
        legend_title="Legend",
    )

    return fig


@helpers.trace_function("Active cases and quarantined percentage graph")
def active_quarantined_percentage_chart(df, days_no):
    fig = go.Figure()

    fig.add_traces(
        go.Scatter(
            x=df[DATE][-days_no:],
            y=df[QUARANTINED_PERCENTAGE][-days_no:],
            mode=MODE_LINES_N_MARKERS,
            name="Quarantined [%]",
        )
    )

    fig.add_traces(
        go.Bar(
            x=df[DATE][-days_no:],
            y=df[ACTIVE_PERCENTAGE][-days_no:],
            name="Active [%]",
        )
    )
    fig.update_layout(
        title="Poland active cases [%] of population",
        legend_title="Legend",
        yaxis_title="[%] of total population",
    )
    return fig


@helpers.trace_function("Cases and active graph")
def cases_and_active(df, days_no, title):
    fig = go.Figure()

    fig.add_traces(
        go.Bar(
            x=df[DATE][-days_no:],
            y=df[CONFIRMED_DAILY][-days_no:],
            name="Confirmed",
        )
    )
    fig.add_traces(
        go.Scatter(
            x=df[DATE][-days_no:],
            y=df[ACTIVE][-days_no:],
            mode=MODE_LINES_N_MARKERS,
            name="Active",
        )
    )

    fig.update_layout(
        title=title,
        legend_title="Legend",
    )

    return fig


@helpers.trace_function("Deaths and recovered graph")
def deaths_and_recovered(df, days_no, title):
    fig = go.Figure()

    fig.add_traces(
        go.Scatter(
            x=df[DATE][-days_no:],
            y=df[RECOVERED][-days_no:],
            mode=MODE_LINES_N_MARKERS,
            name="Recovered",
        )
    )
    fig.add_traces(
        go.Scatter(
            x=df[DATE][-days_no:],
            y=df[DEATHS_DAILY][-days_no:],
            mode=MODE_LINES_N_MARKERS,
            name="Deaths",
        )
    )

    fig.update_layout(
        title=title,
        legend_title="Legend",
    )

    return fig


@helpers.trace_function("Quarantined graph")
def quarantined(df, days_no, title):
    fig_tested = go.Figure()

    fig_tested.add_traces(
        go.Scatter(
            x=df[DATE][-days_no:],
            y=df[QUARANTINED][-days_no:],
            mode=MODE_LINES_N_MARKERS,
            name="Quarantined",
        )
    )

    fig_tested.update_layout(
        title=title,
        legend_title="Legend",
    )

    return fig_tested
