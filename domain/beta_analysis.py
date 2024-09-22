from calendar import month

from dash import html, dcc
from raw.chart_layout import get_layout
from raw.colors import get_color
import statistics
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

config = {"displayModeBar": False}

chart_layout = get_layout(palette="light")


def calculate_percentage_change(df):
    df = df.sort_values("date")
    start_price = df["adjClose"].iloc[0]
    df["rolling_change"] = (df["adjClose"] - start_price) / start_price * 100
    return df


def update_beta_analysis_charts(price_data, market_data, ticker):

    # trim price data based on available market data
    min_date = market_data["Date"].min()
    price_data = price_data.loc[price_data["date"] >= min_date]

    # make col names the same
    market_data = market_data.rename(
        columns={"Date": "date", "Adj Close": "adjClose", "return": "changePercent"}
    )

    # calculate % change
    price_data = calculate_percentage_change(price_data)
    market_data = calculate_percentage_change(market_data)

    # merge data
    returns = pd.merge(
        price_data, market_data, on="date", suffixes=(f"_{ticker}", "_SP500")
    )

    # for beta calculations we use month end values
    # fill nas
    returns_dated = returns.set_index("date")
    month_end_data = returns_dated.resample("BM").last()

    # get monthly returns
    month_end_data["monthly_return_SP500"] = (
        month_end_data["adjClose_SP500"].pct_change() * 100
    )
    month_end_data[f"monthly_return_{ticker}"] = (
        month_end_data[f"adjClose_{ticker}"].pct_change() * 100
    )

    # fill nas
    month_end_data["monthly_return_SP500"] = month_end_data[
        "monthly_return_SP500"
    ].fillna(0)
    month_end_data[f"monthly_return_{ticker}"] = month_end_data[
        f"monthly_return_{ticker}"
    ].fillna(0)

    # calculate beta, stddev + alpha
    X = np.array(month_end_data["monthly_return_SP500"]).reshape(-1, 1)
    y = np.array(month_end_data[f"monthly_return_{ticker}"])

    # calculate beta, alpha + stddev
    model = LinearRegression()
    model.fit(X, y)
    beta = model.coef_[0]
    alpha = model.intercept_
    stddev = statistics.stdev(y)

    # add regression line data for chart
    month_end_data["trend_line"] = month_end_data["monthly_return_SP500"].apply(
        lambda x: (x * beta) + alpha
    )

    change_chart = go.Figure(
        go.Scatter(
            x=returns["date"],
            y=returns[f"rolling_change_{ticker}"],
            mode="lines",
            line=dict(color=get_color("pink"), width=2),
            name=f"{ticker.upper()}",
            hovertemplate="%{y:.2f}%",
        )
    )

    change_chart.add_trace(
        go.Scatter(
            x=returns["date"],
            y=returns["rolling_change_SP500"],
            mode="lines",
            line=dict(color=get_color("purple"), width=2),
            name="S&P500",
            hovertemplate="%{y:.2f}%",
        )
    )

    change_chart.update_layout(
        **chart_layout,
        hovermode="x unified",
        hoverlabel=dict(
            font_color=get_color("black"),
            bordercolor=get_color("black"),
            bgcolor=get_color("white"),
        ),
        yaxis_ticksuffix="%",
        yaxis_tickformat=".0f",
    )

    change_chart.update_xaxes(
        spikecolor=get_color("black"),
    )

    beta_chart = go.Figure(
        go.Scatter(
            x=month_end_data["monthly_return_SP500"],
            y=month_end_data[f"monthly_return_{ticker}"],
            mode="markers",
            marker=dict(color=get_color("orange")),
        )
    )

    beta_chart.add_trace(
        go.Scatter(
            x=month_end_data["monthly_return_SP500"],
            y=month_end_data["trend_line"],
            mode="lines",
            line=dict(color=get_color("red")),
        )
    )

    beta_chart.update_layout(
        **chart_layout,
        xaxis_title="S&P500",
        yaxis_title=f"{ticker.upper()}",
        showlegend=False,
        hovermode=False,
    )

    beta_kpis = html.Div(
        [
            html.Div(
                [
                    html.P("Beta", className="kpi-header"),
                    html.P(f"{beta:.2f}", className="kpi-value"),
                ],
                className="kpi-child",
            ),
            html.Div(
                [
                    html.P("StdDev", className="kpi-header"),
                    html.P(f"{stddev:.2f}", className="kpi-value"),
                ],
                className="kpi-child",
            ),
            html.Div(
                [
                    html.P("Alpha", className="alpha-header"),
                    html.P(f"{alpha:.2f}", className="kpi-value"),
                ],
                className="kpi-child",
            ),
        ],
        className="beta-kpis",
    )

    return [
        html.Div(
            [
                html.H2("Beta Analysis"),
                html.Div(
                    [
                        html.Div([
                            html.H3("5y % change vs. S&P500"),
                            dcc.Graph(figure=change_chart, config=config)],
                            className="change-chart",
                        ),
                        html.Div([
                            html.H3("5y month-end beta analysis"),
                            dcc.Graph(figure=beta_chart, config=config)],
                            className="beta-chart",
                        ),
                        html.Div(beta_kpis, className="beta-kpi-chart"),
                    ],
                    className="beta-analysis",
                )
            ],
            className="light",
        )
    ]
