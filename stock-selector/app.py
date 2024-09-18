from dash import Dash, html, dcc, Input, Output
from raw.get_market_data import get_market_data
from raw.get_profile_data import get_profile_data
from raw.get_price_data import get_price_data
from raw.get_cashflow_data import get_cashflow_data
from domain.kpi_charts import update_kpi_charts
from domain.main_charts import update_charts
from domain.cashflow_charts import update_cashflow_charts
import pandas as pd


# define config for charts
config = {"displayModeBar": False}

# initialise app
app = Dash(__name__)

# define layout
app.layout = html.Div(
    [
        html.Div(html.H1("Stock Analysis"), className="app-title"),
        html.Div(
            dcc.Input(id="ticker", type="text", placeholder="enter ticker..."),
            className="input-ticker",
        ),
        html.Div(id="company-overview"),
        dcc.Store(id="store-data"),  # store data here
        dcc.Slider(
            id="year-slider",
            min=2019,
            max=2023,
            value=2023,
            marks={i: str(i) for i in range(2019, 2024)},
            step=1,
        ),
        html.Div(id="main-charts"),
        html.Div(id="cashflow-charts"),
    ]
)


# get API data
@app.callback(
    Output("store-data", "data"),
    Input("ticker", "value"),
)
def get_all_data(ticker):
    if not ticker:
        return {}
    else:
        # get required data
        profile_data = get_profile_data(ticker)
        price_data = get_price_data(ticker)
        ticker_data = get_market_data(ticker)
        cashflow_data = get_cashflow_data(ticker)

        profile_data_dict = profile_data.to_dict()
        price_data_dict = price_data.to_dict(orient="records")
        ticker_data_dict = ticker_data.to_dict(orient="records")
        cashflow_data_dict = cashflow_data.to_dict()

    return {
        "profile_data": profile_data_dict,
        "price_data": price_data_dict,
        "ticker_data": ticker_data_dict,
        "cashflow_data": cashflow_data_dict,
    }


# update company overview
@app.callback(
    Output("company-overview", "children"),
    Input("store-data", "data"),
)
def update_company_overview(data):
    profile_data = pd.Series(data["profile_data"])
    price_data = pd.DataFrame(data["price_data"])
    ticker_data = pd.DataFrame(data["ticker_data"])
    children = update_kpi_charts(profile_data, price_data, ticker_data)
    return html.Div(children)


# update main charts
@app.callback(
    Output("main-charts", "children"),
    Input("store-data", "data"),
    Input("year-slider", "value"),
)
def update_main_charts(data, year):

    ticker_data = pd.DataFrame(data["ticker_data"])

    # get currency
    currency = ticker_data["currency_symbol"].values[0]

    children = update_charts(ticker_data, currency, year)
    return html.Div(children)


# update cashflow charts
@app.callback(
    Output("cashflow-charts", "children"),
    Input("store-data", "data"),
    Input("year-slider", "value"),
)
def update_cashflow_analysis(data, year):
    cashflow_data = pd.DataFrame(data["cashflow_data"])

    # get currency
    currency = cashflow_data["currency_symbol"].values[0]

    children = update_cashflow_charts(cashflow_data, currency, year)
    return html.Div(children)


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
