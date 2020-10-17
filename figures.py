from plotly.subplots import make_subplots
import plotly.graph_objects as go
import helpers
import poland_stats as pl


MODE_LINES_N_MARKERS = "lines+markers"


@helpers.trace_function("Active cases percentage graph")
def active_percentage(df, days_no, title):
    fig = go.Figure()

    fig.add_traces(
        go.Bar(
            x=df["Date"][-days_no:],
            y=df["Active percentage"][-days_no:],
            name="Active percentage",
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
            x=df["Date"][-days_no:],
            y=df["Quarantined percentage"][-days_no:],
            mode="lines+markers",
            name="Quarantined",
        )
    )
        
    fig.add_traces(
        go.Bar(
            x=df["Date"][-days_no:],
            y=df["Active percentage"][-days_no:],
            name="Active",
        )
    )
    fig.update_layout(
        title='Poland active cases [%] of population',
        legend_title="Legend",
        yaxis_title="[%] of total population"
    )
    return fig


@helpers.trace_function("Cases and active graph")
def cases_and_active(df, days_no, title):
    fig = go.Figure()

    fig.add_traces(
        go.Bar(
            x=df["Date"][-days_no:],
            y=df["Confirmed daily"][-days_no:],
            name="Confirmed",
        )
    )
    fig.add_traces(
        go.Scatter(
            x=df["Date"][-days_no:],
            y=df["Active"][-days_no:],
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
            x=df["Date"][-days_no:],
            y=df["Recovered"][-days_no:],
            mode=MODE_LINES_N_MARKERS,
            name="Recovered",
        )
    )
    fig.add_traces(
        go.Scatter(
            x=df["Date"][-days_no:],
            y=df["Deaths daily"][-days_no:],
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
            x=df["Date"][-days_no:],
            y=df["Quarantined"][-days_no:],
            mode="lines+markers",
            name="Quarantined",
        )
    )

    fig_tested.update_layout(
        title=title,
        legend_title="Legend",
    )

    return fig_tested


@helpers.trace_function("Case distribution graph")
def case_distribution(data: list, title: str) -> go.Figure:
    fig = go.Figure()

    try:
        fig.add_trace(
            go.Scatter(
                x=[i["dateRep"] for i in data],
                y=[i["hospital_rate"] for i in data],
                mode=MODE_LINES_N_MARKERS,
                name="hospital rate",
            )
        )
    except KeyError:
        print(f"Skipping hospital admittion rates due to missing data")

    fig.add_trace(
        go.Scatter(
            x=[i["dateRep"] for i in data], y=[i["deaths"] for i in data], name="deaths"
        )
    )

    fig.add_trace(
        go.Bar(
            x=[i["dateRep"] for i in data], y=[i["cases"] for i in data], name="cases"
        )
    )

    fig.update_layout(
        title=title,
        yaxis_title="daily increase",
        legend_title="Legend",
    )

    return fig


@helpers.trace_function("Case distribution multi-graph")
def case_distribution_subplots(data: list, country_labels: list, title: str) -> go.Figure:

    assert len(data) == len(country_labels)
    N = len(country_labels)

    fig = make_subplots(
        rows=len(country_labels),
        cols=1,
        subplot_titles=country_labels,
        shared_xaxes=True,
        vertical_spacing=0.05,
    )

    date_rep_counter = {}
    for d in data:
        for i in d:
            date_rep_counter[i["dateRep"]] = date_rep_counter.get(i["dateRep"], 0) + 1

    dateRep_common = [k for k, v in date_rep_counter.items() if v == N]

    for n in range(0, N):

        fig.add_trace(
            go.Scatter(
                x=[i["dateRep"] for i in data[n] if i["dateRep"] in dateRep_common],
                y=[
                    i["hospital_rate"]
                    for i in data[n]
                    if i["dateRep"] in dateRep_common
                ],
                mode=MODE_LINES_N_MARKERS,
                name=f"{country_labels[n]} hospital rate",
            ),
            row=n + 1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=[i["dateRep"] for i in data[n] if i["dateRep"] in dateRep_common],
                y=[i["deaths"] for i in data[n] if i["dateRep"] in dateRep_common],
                mode=MODE_LINES_N_MARKERS,
                name=f"{country_labels[n]} deaths",
            ),
            row=n + 1,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                x=[i["dateRep"] for i in data[n] if i["dateRep"] in dateRep_common],
                y=[i["cases"] for i in data[n] if i["dateRep"] in dateRep_common],
                name=f"{country_labels[n]} cases",
            ),
            row=n + 1,
            col=1,
        )
    fig.update_layout(height=1200, width=1000, title_text=title)
    return fig

