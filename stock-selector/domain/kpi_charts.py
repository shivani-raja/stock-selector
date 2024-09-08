import plotly.graph_objects as go
from dash import html, dcc
from datetime import datetime

config = {"displayModeBar": False}


def update_kpi_charts(profile_data):
    # create KPI charts
    kpi_charts = go.Figure()

    # current price
    kpi_charts.add_trace(
        go.Indicator(
            value=profile_data["price"],
            number={"prefix": profile_data["currency_symbol"]},
            title={"text": "Current Price"},
            domain={"row": 0, "column": 0},
        )
    )

    # market cap
    kpi_charts.add_trace(
        go.Indicator(
            value=profile_data["mktCap"],
            number={"prefix": profile_data["currency_symbol"]},
            title={"text": "Market Cap"},
            domain={"row": 0, "column": 1},
        )
    )

    # beta
    kpi_charts.add_trace(
        go.Indicator(
            value=profile_data["beta"],
            title={"text": "Beta"},
            domain={"row": 0, "column": 2},
        )
    )

    # add ipo date
    kpi_charts.add_trace(
        go.Indicator(
            value=datetime.strptime(profile_data["ipoDate"], "%Y-%m-%d").year,
            title={"text": "IPO Date"},
            domain={"row": 0, "column": 3},
        )
    )

    kpi_charts.update_layout(
        template="ggplot2",
        font_family="Inter",
        grid={"rows": 1, "columns": 4, "pattern": "independent"},
        height=250,
    )

    return [
                html.H1(profile_data["companyName"]),
                html.Img(src=profile_data["image"]),
                html.H2("Company Overview"),
                html.P(profile_data["description"]),
                dcc.Graph(figure=kpi_charts, config=config),
    ]
