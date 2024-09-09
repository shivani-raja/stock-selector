from dash import Dash, html, dcc, Input, Output
from raw.get_market_data import get_market_data
from raw.get_profile_data import get_profile_data
from raw.get_price_data import get_price_data
from domain.kpi_charts import update_kpi_charts
from domain.main_charts import update_charts


# define config for charts
config = {"displayModeBar": False}

# initialise app
app = Dash(__name__)

# define layout
app.layout = html.Div(
    [
        html.Div(
            dcc.Input(id="ticker", type="text", placeholder="Enter ticker symbol"),
            className="input-ticker",
        ),
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
        # get required data
        profile_data = get_profile_data(ticker)
        price_data = get_price_data(ticker)
        children = update_kpi_charts(profile_data, price_data)
        return html.Div(children)


# update graphs
@app.callback(
    Output("graphs-container", "children"),
    Input("ticker", "value"),
    Input("year-slider", "value"),
)
def update_main_charts(ticker, year):

    if not ticker:
        return {}
    else:
        # get market data
        ticker_data = get_market_data(ticker)

        # get currency
        currency = ticker_data["currency_symbol"].values[0]

        children = update_charts(ticker_data, currency, year)
        return html.Div(children)


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
