import requests
import pandas as pd
from raw.currency_symbols import get_currency_symbols


def get_market_data(ticker):
    """gets stock market data from financial modelling prep API

    :return: ticker_data, financial statement data for the past 5 years
    """

    # api key
    api_key = "52a44d5f713429851c9f7961317e6877"

    # get data
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=annual&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ticker_data = pd.json_normalize(data)

        # add currency symbol for chart labels
        currency_symbols = get_currency_symbols()
        currency = ticker_data["reportedCurrency"].values[0]
        ticker_data["currency_symbol"] = currency_symbols.get(currency)

        # convert calendar year to int for charts
        ticker_data["calendarYear"] = ticker_data["calendarYear"].astype(int)

    else:
        print(f"Failed to fetch data for {ticker}: {response.status_code}")
        ticker_data = []

    return ticker_data
