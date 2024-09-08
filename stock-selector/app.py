from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
from raw.get_market_data import get_market_data
from raw.get_sankey_data import get_sankey_data
from raw.get_profile_data import get_profile_data
from domain.kpi_charts import update_kpi_charts


# function to format large numbers for graph labels
def format_number(n):
    if abs(n) >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"  # billions
    elif abs(n) >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"  # millions
    elif abs(n) >= 1_000:
        return f"{n / 1_000:.1f}K"  # thousands
    else:
        return str(n)  # smaller numbers


# define config for charts
config = {"displayModeBar": False}

# initialise app
app = Dash(__name__)

# define layout
app.layout = html.Div(
    [
        dcc.Input(id="ticker", type="text", placeholder="Enter ticker symbol"),
        html.Div(id="company-overview"),
        dcc.Slider(
            id="year-slider",
            min=2019,
            max=2023,
            value=2023,
            marks={i: str(i) for i in range(2019, 2024)},  # Slider marks for years
            step=1,
        ),
        html.Div(id="graphs-container"),
    ]
)


# update company overview
@app.callback(
    Output("company-overview", "children"),
    Input("ticker", "value"),
)
def update_company_overview(ticker):

    if not ticker:
        return {}
    else:
        # get profile data
        profile_data = get_profile_data(ticker)
        children = update_kpi_charts(profile_data)
        return html.Div(children)


# update graphs
@app.callback(
    Output("graphs-container", "children"),
    Input("ticker", "value"),
    Input("year-slider", "value"),
)
def update_charts(ticker, year):

    if not ticker:
        return {}
    else:
        # get market data
        ticker_data = get_market_data(ticker)

        # get currency
        currency = ticker_data["currency_symbol"].values[0]

        # update PnL chart
        pnl_chart = go.Figure(
            data=[
                go.Bar(
                    name="Revenue",
                    x=ticker_data["calendarYear"],
                    y=ticker_data["revenue"],
                    text=[
                        f"{currency}{format_number(val)}"
                        for val in ticker_data["revenue"]
                    ],
                ),
                go.Bar(
                    name="Net Income/Loss",
                    x=ticker_data["calendarYear"],
                    y=ticker_data["netIncome"],
                    text=[
                        f"{currency}{format_number(val)}"
                        for val in ticker_data["netIncome"]
                    ],
                ),
            ]
        )
        pnl_chart.update_layout(
            barmode="group",
            template="ggplot2",
            yaxis_tickprefix=currency,
            font_family="Inter",
            hovermode=False,
            legend=dict(
                orientation="h",
                yanchor="top",
                x=0.5,
            ),
        )

        # update sankey chart
        sankey_data = get_sankey_data(ticker_data)
        sankey_data = sankey_data[sankey_data["year"] == year]

        sankey_chart = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=15,
                        line=dict(color="black", width=0.5),
                        x=sankey_data["x"],
                        y=sankey_data["y"],
                        label=sankey_data["label"],
                    ),
                    # Add links
                    link=dict(
                        source=sankey_data["source"],
                        target=sankey_data["target"],
                        value=sankey_data["value"],
                    ),
                )
            ]
        )

        sankey_chart.update_layout(
            template="ggplot2",
            font_family="Inter",
            hovermode=False,
        )

        return [
            dcc.Graph(figure=pnl_chart, config=config),
            dcc.Graph(figure=sankey_chart, config=config),
        ]


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
