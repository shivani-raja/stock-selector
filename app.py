import pandas as pd
from datetime import datetime
from dash import Dash, html, dcc, Input, Output, callback_context

from raw.get_ticker_data import get_ticker_data
from raw.get_market_data import get_market_data
from raw.time_of_day import time_of_day
from domain.company_overview import update_company_overview_charts
from domain.latest_performance_charts import update_latest_performance_charts
from domain.yearly_performance_charts import update_yearly_performance_charts
from domain.beta_analysis import update_beta_analysis_charts


# define config for charts
config = {"displayModeBar": False}

# initialise app
app = Dash(__name__,  suppress_callback_exceptions=True)
app.title = "Stock Analysis"
server = app.server

# get greeting
greeting = time_of_day()

# define layout
app.layout = html.Div(
    [
        # data store
        dcc.Store(id="store-data"),
        # intro section
        html.Div(
            [
                html.H1(greeting, className="greeting"),
                html.Div(
                    [
                        dcc.Input(
                            id="ticker", type="text", placeholder="enter ticker..."
                        ),
                        html.Button("⌕", id="search-button", n_clicks=0),
                    ],
                    className="search-box",
                ),
                html.Div(id="error-message", className="error-message"),
            ],
            className="light",
        ),
        # company overview
        html.Div(id="company-overview"),
        # latest performance
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            id="latest-performance-title",
                            className="latest-performance-title",
                        ),
                        html.Div(
                            id="year-slider-container",
                            className="year-slider-container",
                        ),
                    ],
                    className="latest-performance-intro",
                ),
                html.Div(id="latest-performance"),
            ],
            className="light",
        ),
        # 5y performance
        html.Div(id="yearly-performance"),
        # beta analysis
        html.Div(id="beta-analysis"),
    ]
)


@app.callback(
    [Output("store-data", "data"),
     Output("error-message", "children")],
    Input("search-button", "n_clicks"),
    Input("ticker", "value"),
)
def get_all_data(n_clicks, ticker):
    if n_clicks > 0:
        if not ticker:
            return {}
        else:
            # get required data
            data, error_message = get_ticker_data(ticker)

    else:
        data = []
        error_message = []
    return data, html.P(error_message)


@app.callback(
    Output("year-slider-container", "children"),
    Input("store-data", "data"),
)
def update_slider(data):
    if data:
        return dcc.Slider(
            min=datetime.now().year - 5,
            max=datetime.now().year,
            step=1,
            value=datetime.now().year,
            marks={year: str(year) for year in range(datetime.now().year - 5, datetime.now().year)},
            id="year-slider",
        )
    else:
        return []


# update company overview
@app.callback(
    Output("company-overview", "children"),
    Input("store-data", "data"),
)
def update_company_overview(data):

    if data:
        # get data
        profile_data = pd.read_json(data["profile_data"], orient="split").squeeze()
        price_data = pd.read_json(data["price_data"], orient="split")

        children = update_company_overview_charts(profile_data, price_data)
        return html.Div(children)
    else:
        return []


# update latest performance
@app.callback(
    [
        Output("latest-performance", "children"),
        Output("latest-performance-title", "children"),
    ],
    Input("store-data", "data"),
    Input("year-slider", "value"),
)
def update_latest_performance(data, year):
    if year and data:
        triggered = callback_context.triggered
        if triggered and "year-slider" in triggered[0]["prop_id"]:
            # get data
            sankey_nodes = pd.read_json(data["sankey_nodes"], orient="split")
            sankey_links = pd.read_json(data["sankey_links"], orient="split")
            cashflow_data = pd.read_json(data["cashflow_data"], orient="split")

            children = update_latest_performance_charts(
                sankey_nodes, sankey_links, cashflow_data, year
            )
            return html.Div(children), html.H2(f"Latest Performance")
    else:
        return [], []


# update 5y performance
@app.callback(
    Output("yearly-performance", "children"),
    Input("store-data", "data"),
)
def update_yearly_performance(data):

    if data:
        # get data
        income_statement_data = pd.read_json(data["income_statement_data"], orient="split")
        price_data = pd.read_json(data["price_data"], orient="split")

        children = update_yearly_performance_charts(income_statement_data, price_data)
        return html.Div(children)
    else:
        return []


# update beta analysis
@app.callback(
    Output("beta-analysis", "children"),
    Input("store-data", "data"),
    Input("ticker", "value"),
)
def update_beta_analysis(data, ticker):

    if data:
        # get data
        price_data = pd.read_json(data["price_data"], orient="split")
        market_data = get_market_data()

        children = update_beta_analysis_charts(price_data, market_data, ticker)
        return html.Div(children)
    else:
        return []


# Run the Dash app
if __name__ == "__main__":
    app.run(debug=True)
