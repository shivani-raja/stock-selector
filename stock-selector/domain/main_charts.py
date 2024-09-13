from raw.format_number import format_number
from raw.get_sankey_data import get_sankey_data
import plotly.graph_objects as go
from dash import dcc, html

config = {"displayModeBar": False}


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
        barmode="group",
        barcornerradius=8,
        yaxis_tickprefix=currency,
        font_family="Inter",
        hovermode=False,
        legend=dict(
            orientation="h",
            yanchor="top",
            x=0.5,
        ),
        paper_bgcolor="#1A2038",
        plot_bgcolor="#1A2038",
        font_color="#FFFFFF",
        uniformtext_minsize=5,
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
                    x=sankey_nodes['x'],
                    y=sankey_nodes['y'],
                    color=sankey_nodes['color'],
                    label=sankey_nodes['label'],

                ),
                # Add links
                link=dict(
                    source=sankey_links["source"],
                    target=sankey_links["target"],
                    value=sankey_links["value"],
                    color=sankey_links['color'],
                ),
            )
        ]
    )

    sankey_chart.update_layout(
        font_family="Inter",
        hovermode=False,
        paper_bgcolor="#1A2038",
        plot_bgcolor="#1A2038",
        font_color="#FFFFFF",
    )

    sankey_chart.update_yaxes(
        linecolor="#243780", gridcolor="#243780", zerolinecolor="#243780"
    )
    sankey_chart.update_xaxes(
        linecolor="#243780", gridcolor="#243780", zerolinecolor="#243780"
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
            ],
            className="main-charts-1",
        )
    ]
