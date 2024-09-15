from dash import html, dcc
from raw.format_number import format_number
from datetime import datetime
import plotly.graph_objects as go

config = {"displayModeBar": False}


def update_kpi_charts(profile_data, price_data, ticker_data):

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
        increasing_line_color="#4BDB95",
        decreasing_line_color="#FF3B4C",
    )

    price_chart.update_layout(
        paper_bgcolor="#1A2038",
        plot_bgcolor="#1A2038",
        font_family="Inter",
        font_color="#FFFFFF",
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(label="5y", step="all"),
                    ]
                )
            ),
            type="date",
        ),
        xaxis_rangeslider_visible=False,
        yaxis_tickprefix=profile_data.currency_symbol,
        hovermode="x unified",
        hoverlabel=dict(
            font_color="#131526",
            bordercolor="#131526",
            bgcolor="#FFFFFF",
        ),
    )

    price_chart.update_yaxes(
        linecolor="#243780", gridcolor="#243780", zerolinecolor="#243780"
    )
    price_chart.update_xaxes(
        linecolor="#243780",
        gridcolor="#243780",
        zerolinecolor="#243780",
        rangeselector_bgcolor="#243780",
    )
    # trim ticker data
    ticker_data = ticker_data.iloc[ticker_data["calendarYear"].idxmax()]

    # create KPI charts
    return [
        html.Div(
            [
                html.Div(
                    [
                        html.H1(profile_data["companyName"]),
                        dcc.Graph(figure=price_chart, config=config),
                    ],
                    className="overview-chart",
                ),
                html.Div(
                    [
                        html.Img(src=profile_data["image"]),
                        html.H2("Company Overview"),
                        html.P(f"{profile_data.description[:1000]}..."),
                    ],
                    className="overview-metrics",
                ),
            ],
            className="company-overview",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P("Current Price", className="kpi-header-a"),
                        html.P(
                            f"{profile_data.currency_symbol}{profile_data.price}",
                            className="kpi-value",
                        ),
                    ],
                    className="kpi-child",
                ),
                html.Div(
                    [
                        html.P("DCF", className="kpi-header-b"),
                        html.P(
                            f"{profile_data.currency_symbol}{profile_data.dcf:.2f}",
                            className="kpi-value",
                        ),
                    ],
                    className="kpi-child",
                ),
                html.Div(
                    [
                        html.P("Market Cap", className="kpi-header-a"),
                        html.P(
                            f"{profile_data.currency_symbol}{format_number(profile_data.mktCap)}",
                            className="kpi-value",
                        ),
                    ],
                    className="kpi-child",
                ),
                html.Div(
                    [
                        html.P("Beta", className="kpi-header-b"),
                        html.P(f"{profile_data.beta}", className="kpi-value"),
                    ],
                    className="kpi-child",
                ),
                html.Div(
                    [
                        html.P("EPS", className="kpi-header-a"),
                        html.P(f"{ticker_data.eps}", className="kpi-value"),
                    ],
                    className="kpi-child",
                ),
                html.Div(
                    [
                        html.P("IPO Date", className="kpi-header-b"),
                        html.P(
                            f"{datetime.strptime(profile_data.ipoDate,'%Y-%m-%d').strftime('%d/%m/%Y')}",
                            className="kpi-value",
                        ),
                    ],
                    className="kpi-child",
                ),
                html.Div(
                    [
                        html.P("Sector", className="kpi-header-a"),
                        html.P(f"{profile_data.sector}", className="kpi-value"),
                    ],
                    className="kpi-child",
                ),
                html.Div(
                    [
                        html.P("Country", className="kpi-header-b"),
                        html.P(f"{profile_data.country}", className="kpi-value"),
                    ],
                    className="kpi-child",
                ),
                html.Div(
                    [
                        html.P("CEO", className="kpi-header-a),
                        html.P(f"{profile_data.ceo}", className="kpi-value"),
                    ],
                    className="kpi-child",
                ),
                html.Div(
                    [
                        html.P("Exchange", className="kpi-header-b"),
                        html.P(
                            f"{profile_data.exchangeShortName}", className="kpi-value"
                        ),
                    ],
                    className="kpi-child",
                ),
            ],
            className="kpi-charts",
        ),
    ]
