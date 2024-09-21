from raw.format_number import format_number
from raw.chart_layout import get_layout
from raw.colors import get_color
import plotly.graph_objects as go
from dash import dcc, html

config = {"displayModeBar": False}

chart_layout = get_layout(palette="dark")


def update_yearly_performance_charts(income_statement_data, price_data):

    # get currency
    currency = income_statement_data["currency_symbol"].values[0]

    # colour cols based on PnL
    income_statement_data["color"] = income_statement_data.apply(
        lambda row: (
            get_color("red") if int(row["netIncome"]) < 0 else get_color("green")
        ),
        axis=1,
    )

    # update PnL chart
    pnl_chart = go.Figure(
        data=[
            go.Bar(
                name="Revenue",
                x=income_statement_data["calendarYear"],
                y=income_statement_data["revenue"],
                text=[
                    f"{currency}{format_number(val)}"
                    for val in income_statement_data["revenue"]
                ],
                textposition="outside",
                marker={"color": get_color("purple"), "line_width": 0},
            ),
            go.Bar(
                name="Net Income/Loss",
                x=income_statement_data["calendarYear"],
                y=income_statement_data["netIncome"],
                text=[
                    f"{currency}{format_number(val)}"
                    for val in income_statement_data["netIncome"]
                ],
                textposition="outside",
                marker={"color": income_statement_data["color"], "line_width": 0},
            ),
        ]
    )
    pnl_chart.update_layout(
        barmode="group",
        barcornerradius=8,
        yaxis_tickprefix=currency,
        **chart_layout,
        hovermode=False,
    )

    # update ratio chart
    ratio_chart = go.Figure(
        go.Scatter(
            x=income_statement_data["calendarYear"],
            y=income_statement_data["grossProfitRatio"],
            mode="lines+markers",
            line=dict(color=get_color("red"), width=2),
            name="Gross Profit Margin",
            hovertemplate="%{y:.2f}%",
        )
    )
    ratio_chart.add_trace(
        go.Scatter(
            x=income_statement_data["calendarYear"],
            y=income_statement_data["operatingIncomeRatio"],
            mode="lines+markers",
            line=dict(color=get_color("orange"), width=2),
            name="Operating Profit Margin",
            hovertemplate="%{y:.2f}%",
        )
    )
    ratio_chart.add_trace(
        go.Scatter(
            x=income_statement_data["calendarYear"],
            y=income_statement_data["netIncomeRatio"],
            mode="lines+markers",
            line=dict(color=get_color("pink"), width=2),
            name="Net Profit Margin",
            hovertemplate="%{y:.2f}%",
        )
    )

    ratio_chart.update_layout(
        **chart_layout,
        hovermode="x unified",
        hoverlabel=dict(
            font_color=get_color("black"),
            bordercolor=get_color("black"),
            bgcolor=get_color("white"),
        ),
        yaxis_ticksuffix="%",
        yaxis_tickformat=".2f",
    )

    ratio_chart.update_xaxes(
        spikecolor=get_color("black"),
    )

    # format price data for returns chart

    return [
        html.Div(
            [
                html.H2("5 Year Performance"),
                html.Div(
                    [
                        html.Div([
                            html.H3("5y revenue + profit/loss"),
                            dcc.Graph(figure=pnl_chart, config=config)],
                            className="pnl-chart",
                        ),
                        html.Div([
                            html.H3("5y profitability margins"),
                            dcc.Graph(figure=ratio_chart, config=config)],
                            className="ratio-chart",
                        ),
                    ],
                    className="yearly-performance-charts",
                ),
            ],
            className="dark",
        )
    ]
