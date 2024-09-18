from raw.format_number import format_number
from raw.get_sankey_data import get_sankey_data
import plotly.graph_objects as go
from dash import dcc, html

config = {"displayModeBar": False}

chart_layout = {
    "paper_bgcolor": "#1A2038",
    "plot_bgcolor": "#1A2038",
    "font_family": "Inter",
    "font_color": "#FFFFFF",
    "xaxis": {
        "linecolor": "#243780",
        "gridcolor": "#243780",
        "zerolinecolor": "#243780",
    },
    "yaxis": {
        "linecolor": "#243780",
        "gridcolor": "#243780",
        "zerolinecolor": "#243780",
    },
    "legend": {
        "orientation": "h",
        "yanchor": "top",
        "x": 0.25,
    },
}


def update_charts(ticker_data, currency, year):
    # update PnL chart
    pnl_chart = go.Figure(
        data=[
            go.Bar(
                name="Revenue",
                x=ticker_data["calendarYear"],
                y=ticker_data["revenue"],
                text=[
                    f"{currency}{format_number(val)}" for val in ticker_data["revenue"]
                ],
                textposition="outside",
                marker={"color": "#588AFF", "line_width": 0},
            ),
            go.Bar(
                name="Net Income/Loss",
                x=ticker_data["calendarYear"],
                y=ticker_data["netIncome"],
                text=[
                    f"{currency}{format_number(val)}"
                    for val in ticker_data["netIncome"]
                ],
                textposition="outside",
                marker={"color": ticker_data["color"], "line_width": 0},
            ),
        ]
    )
    pnl_chart.update_layout(
        title=dict(text="5y Performance", x=0.5, xanchor="center"),
        barmode="group",
        barcornerradius=8,
        yaxis_tickprefix=currency,
        **chart_layout,
        hovermode=False,
    )

    pnl_chart.update_yaxes(
        linecolor="#243780", gridcolor="#243780", zerolinecolor="#243780"
    )
    pnl_chart.update_xaxes(
        linecolor="#243780", gridcolor="#243780", zerolinecolor="#243780"
    )

    # update sankey chart
    sankey_nodes, sankey_links = get_sankey_data(ticker_data, currency)
    sankey_nodes = sankey_nodes[sankey_nodes["year"] == year]
    sankey_links = sankey_links[sankey_links["year"] == year]

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
        title=dict(text=f"Sankey {year}", x=0.5, xanchor="center"),
        **chart_layout,
        hovermode=False,
    )

    sankey_chart.update_yaxes(
        linecolor="#243780", gridcolor="#243780", zerolinecolor="#243780"
    )
    sankey_chart.update_xaxes(
        linecolor="#243780", gridcolor="#243780", zerolinecolor="#243780"
    )

    # update ratio chart
    ratio_chart = go.Figure(
        go.Scatter(
            x=ticker_data["calendarYear"],
            y=ticker_data["grossProfitRatio"],
            mode="lines+markers",
            line=dict(color="#FF3B4C", width=2),
            name="Gross Profit Margin",
            hovertemplate="%{y:.2f}%",
        )
    )
    ratio_chart.add_trace(
        go.Scatter(
            x=ticker_data["calendarYear"],
            y=ticker_data["operatingIncomeRatio"],
            mode="lines+markers",
            line=dict(color="#FF7C58", width=2),
            name="Operating Profit Margin",
            hovertemplate="%{y:.2f}%",
        )
    )
    ratio_chart.add_trace(
        go.Scatter(
            x=ticker_data["calendarYear"],
            y=ticker_data["netIncomeRatio"],
            mode="lines+markers",
            line=dict(color="#FF72D9", width=2),
            name="Net Profit Margin",
            hovertemplate="%{y:.2f}%",
        )
    )

    ratio_chart.update_layout(
        title=dict(text=f"Margins over 5y", x=0.5, xanchor="center"),
        **chart_layout,
        hovermode="x unified",
        hoverlabel=dict(
            font_color="#131526",
            bordercolor="#131526",
            bgcolor="#FFFFFF",
        ),
        yaxis_ticksuffix="%",
        yaxis_tickformat=".2f",
    )

    ratio_chart.update_xaxes(
        spikecolor="#FFFFFF",
    )

    return [
        html.Div(
            [
                html.Div(
                    dcc.Graph(figure=pnl_chart, config=config), className="pnl-chart"
                ),
                html.Div(
                    dcc.Graph(figure=sankey_chart, config=config),
                    className="sankey-chart",
                ),
                html.Div(
                    dcc.Graph(figure=ratio_chart, config=config),
                    className="ratio-chart",
                ),
            ],
            className="main-charts-1",
        )
    ]
