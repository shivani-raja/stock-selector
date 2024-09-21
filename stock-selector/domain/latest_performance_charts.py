from raw.format_number import format_number
from raw.colors import get_color
from raw.chart_layout import get_layout
import plotly.graph_objects as go
from dash import dcc, html

config = {"displayModeBar": False}

chart_layout = get_layout(palette="light")


def update_latest_performance_charts(sankey_nodes, sankey_links, cashflow_data, year):

    # get currency
    currency = cashflow_data.currency_symbol.values[0]

    # filter data on year
    sankey_nodes = sankey_nodes[sankey_nodes["year"] == year].squeeze()
    sankey_links = sankey_links[sankey_links["year"] == year].squeeze()
    cashflow_data = cashflow_data[cashflow_data["calendarYear"] == year].squeeze()

    sankey_chart = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=10,
                    x=sankey_nodes["x"],
                    y=sankey_nodes["y"],
                    color=sankey_nodes["color"],
                    label=sankey_nodes["label"],
                    line=dict(width=0),
                ),
                # Add links
                link=dict(
                    source=sankey_links["source"],
                    target=sankey_links["target"],
                    value=sankey_links["value"],
                    color=sankey_links["color"],
                ),
            )
        ]
    )

    sankey_chart.update_layout(
        **chart_layout,
        hovermode=False,
    )

    sankey_chart.update_yaxes(
        linecolor="#243780", gridcolor="#243780", zerolinecolor="#243780"
    )
    sankey_chart.update_xaxes(
        linecolor="#243780", gridcolor="#243780", zerolinecolor="#243780"
    )

    cashflow_chart = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "total"],
            x=["Cash at Start", "Operations", "Investing", "Financing", "Cash at End"],
            textposition="outside",
            y=[
                cashflow_data.cashAtBeginningOfPeriod,
                cashflow_data.netCashProvidedByOperatingActivities,
                cashflow_data.netCashUsedForInvestingActivites,
                cashflow_data.netCashUsedProvidedByFinancingActivities,
                cashflow_data.cashAtEndOfPeriod,
            ],
            text=[
                f"{currency}{format_number(cashflow_data.cashAtBeginningOfPeriod)}",
                f"{currency}{format_number(cashflow_data.netCashProvidedByOperatingActivities)}",
                f"{currency}{format_number(cashflow_data.netCashUsedForInvestingActivites)}",
                f"{currency}{format_number(cashflow_data.netCashUsedProvidedByFinancingActivities)}",
                f"{currency}{format_number(cashflow_data.cashAtEndOfPeriod)}",
            ],
            connector={"line": {"color": get_color("chart_line_dark")}},
            base=0,
            decreasing={"marker": {"color": get_color("red")}},
            increasing={"marker": {"color": get_color("green")}},
            totals={"marker": {"color": get_color("purple")}},
        )
    )

    cashflow_chart.update_layout(
        **chart_layout,
        yaxis_tickprefix=currency,
        hovermode=False,
    )

    return [
        html.Div(
            [
                html.Div([
                    html.H3(f"Sankey {year}"),
                    dcc.Graph(figure=sankey_chart, config=config)],
                    className="sankey-chart",
                ),
                html.Div([
                    html.H3(f"Cashflow statement {year}"),
                    dcc.Graph(figure=cashflow_chart, config=config)],
                    className="cashflow-chart",
                ),
            ],
            className="latest-performance-charts",
        )
    ]
