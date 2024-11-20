from dash import html, dcc
from raw.format_number import format_number
from raw.chart_layout import get_layout
from raw.colors import get_color
from datetime import datetime
import plotly.graph_objects as go

config = {"displayModeBar": False}

chart_layout = get_layout(palette="dark")


def update_company_overview_charts(profile_data, price_data):

    # extract currency symbol
    currency = profile_data["currency_symbol"]

    # create historical share price chart
    price_chart = go.Figure(
        go.Candlestick(
            x=price_data["date"],
            open=price_data["open"],
            close=price_data["close"],
            high=price_data["high"],
            low=price_data["low"],
        )
    )
    price_chart.update_traces(
        increasing_line_color=get_color("green"),
        decreasing_line_color=get_color("red"),
    )

    price_chart.update_layout(
        **chart_layout,
        height=350,
        xaxis_rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=3, label="3y", step="year", stepmode="backward"),
                    dict(label="All", step="all"),
                ]
            )
        ),
        xaxis_rangeslider_visible=False,
        yaxis_tickprefix=currency,
        hovermode="x unified",
        hoverlabel=dict(
            font_color=get_color("black"),
            bordercolor=get_color("black"),
            bgcolor=get_color("white"),
        ),
    )

    price_chart.update_xaxes(
        rangeselector_bgcolor=get_color("chart_line_dark"),
        spikecolor=get_color("white"),
    )

    kpi_charts = html.Div(
        [
            html.Div(
                [
                    html.P("Country", className="kpi-header"),
                    html.P(f"{profile_data.country}", className="kpi-value"),
                ],
                className="kpi-child",
            ),
            html.Div(
                [
                    html.P("CEO", className="kpi-header"),
                    html.P(f"{profile_data.ceo}", className="kpi-value"),
                ],
                className="kpi-child",
            ),
            html.Div(
                [
                    html.P("Exchange", className="kpi-header"),
                    html.P(f"{profile_data.exchangeShortName}", className="kpi-value"),
                ],
                className="kpi-child",
            ),
            html.Div(
                [
                    html.P("Sector", className="kpi-header"),
                    html.P(f"{profile_data.sector}", className="kpi-value"),
                ],
                className="kpi-child",
            ),
            html.Div(
                [
                    html.P("IPO Date", className="kpi-header"),
                    html.P(
                        f"{datetime.strptime(profile_data.ipoDate, '%Y-%m-%d').strftime('%d/%m/%Y')}",
                        className="kpi-value",
                    ),
                ],
                className="kpi-child",
            ),
            html.Div(
                [
                    html.P("Market Cap", className="kpi-header"),
                    html.P(
                        f"{currency}{format_number(profile_data.mktCap)}",
                        className="kpi-value",
                    ),
                ],
                className="kpi-child",
            ),
        ],
        className="kpi-charts",
    )

    # create KPI charts
    return [
        html.Div(
            [
                html.Div(
                    [
                        html.H2(profile_data["companyName"]),
                        html.P(f"{profile_data.description[:1000]}..."),
                        html.Img(src=profile_data["image"]),
                    ],
                    className="company-overview-intro",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3("Share price history - current price:"),
                                        html.H3(f"{currency}{profile_data.price:.2f}", className="current-price"),
                                    ],
                                    className="current-price-container"
                                ),
                                dcc.Graph(figure=price_chart, config=config),
                            ],
                            className="price-chart",
                        ),
                        html.Div(kpi_charts, className="kpi-chart"),
                    ],
                    className="company-overview-charts",
                ),
            ],
            className="dark",
        ),
    ]
