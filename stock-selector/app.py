from os import times

from dash import Dash, html, dcc, Input, Output
from raw.get_ticker_data import get_ticker_data
from raw.time_of_day import time_of_day
from domain.company_overview import update_company_overview_charts
from domain.main_charts import update_charts
from domain.cashflow_charts import update_cashflow_charts
import pandas as pd


# define config for charts
config = {"displayModeBar": False}

# initialise app
app = Dash(__name__)

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
            ],
            className="light",
        ),
        # company overview
        html.Div(id="company-overview"),
        # 5y performance
        html.Div(
            id="5y-performance", className="light"
        ),  # todo: move these to the corresponding scripts,
        # latest performance
        html.Div(id="latest-performance", className="dark"),
        # beta analysis
        html.Div(id="beta-analysis", className="light"),
    ]
)


# get API data
@app.callback(
    Output("store-data", "data"),
    Input("search-button", "n_clicks"),
    Input("ticker", "value"),
)
def get_all_data(n_clicks, ticker):
    if n_clicks > 0:
        if not ticker:
            return {}
        else:
            # get required data
            data = get_ticker_data(ticker)
    else:
        data = []
    return data


# update company overview
@app.callback(
    Output("company-overview", "children"),
    Input("store-data", "data"),
)
def update_company_overview(data):

    # get data
    profile_data = pd.read_json(data["profile_data"], orient="split").squeeze()
    price_data = pd.read_json(data["price_data"], orient="split")

    children = update_company_overview_charts(profile_data, price_data)
    return html.Div(children)


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
