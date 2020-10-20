
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import common.helpers as helpers

MODE_LINES_N_MARKERS = "lines+markers"

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


@helpers.trace_function("Data timeline multi-graph")
def distribution_subplots(data: list, selected_metrics: list, country_labels: list, title: str) -> go.Figure:

    assert len(data) == len(country_labels)
    assert len(selected_metrics) > 0
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

    date_rep_common = [k for k, v in date_rep_counter.items() if v == N]

    for n in range(0, N):

        for s in selected_metrics:
            fig.add_trace(
                go.Scatter(
                    x=[i["dateRep"] for i in data[n] if i["dateRep"] in date_rep_common],
                    y=[
                        i[s]
                        for i in data[n]
                        if i["dateRep"] in date_rep_common
                    ],
                    mode=MODE_LINES_N_MARKERS,
                    name=f"{country_labels[n]} {s.replace('_',' ')}",
                ),
                row=n + 1,
                col=1,
            )
    fig.update_layout(height=1200, width=1000, title_text=title)
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