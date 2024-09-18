import requests
import pandas as pd
from raw.currency_symbols import get_currency_symbols


def get_cashflow_data(ticker):
    """gets cashflow data from financial modelling prep API

    :return: cashflow_data, a dataset of historical share price
    """

    # api key
    api_key = "52a44d5f713429851c9f7961317e6877"

    # get data
    url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period=annual&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cashflow_data = pd.json_normalize(data)

        # add currency symbol for chart labels
        currency_symbols = get_currency_symbols()
        currency = cashflow_data["reportedCurrency"].values[0]
        cashflow_data["currency_symbol"] = currency_symbols.get(currency)

    else:
        print(f"Failed to fetch data for {ticker}: {response.status_code}")
        cashflow_data = []

    return cashflow_data
