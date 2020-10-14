from plotly.subplots import make_subplots
import plotly.graph_objects as go
import helpers


@helpers.trace_function('Case distribution graph')
def case_distribution(data: list, title: str) -> go.Figure:
    fig = go.Figure()

    try:
        fig.add_trace(
            go.Scatter(
                x=[i["dateRep"] for i in data],
                y=[i["hospital_rate"] for i in data],
                mode="lines+markers",
                name="hospital rate",
            )
        )
    except KeyError:
        print(f'Skipping hospital admittion rates due to missing data')
        

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
        #     xaxis_title="Date",
        #     yaxis_title="Amount",
        legend_title="Legend",
        #     font=dict(
        #         family="Courier New, monospace",
        #         size=18,
        #         color="RebeccaPurple"
        # )
    )
    return fig


@helpers.trace_function('Case distribution multi-graph')
def case_distribution_subplots(data: list, sub_titles: list, title: str) -> go.Figure:

    assert len(data) == len(sub_titles)
    N = len(sub_titles)

    fig = make_subplots(
        rows=len(sub_titles),
        cols=1,
        subplot_titles=sub_titles,
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
                mode="lines+markers",
                name=f"{sub_titles[n]} hospital rate",
            ),
            row=n + 1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=[i["dateRep"] for i in data[n] if i["dateRep"] in dateRep_common],
                y=[i["deaths"] for i in data[n] if i["dateRep"] in dateRep_common],
                name=f"{sub_titles[n]} deaths",
            ),
            row=n + 1,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                x=[i["dateRep"] for i in data[n] if i["dateRep"] in dateRep_common],
                y=[i["cases"] for i in data[n] if i["dateRep"] in dateRep_common],
                name=f"{sub_titles[n]} cases",
            ),
            row=n + 1,
            col=1,
        )
    fig.update_layout(height=900, width=800, title_text=title)
    return fig
