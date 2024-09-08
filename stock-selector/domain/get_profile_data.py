import requests
import pandas as pd
from raw.currency_symbols import get_currency_symbols


def get_profile_data(ticker):
    """gets company profile market data from financial modelling prep API

    :return: profile_data, a dataset of company information
    """

    # api key
    api_key = "52a44d5f713429851c9f7961317e6877"

    # get data
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        profile_data = pd.json_normalize(data)

        # add currency symbol for chart labels
        currency_symbols = get_currency_symbols()
        currency = profile_data["currency"].values[0]
        profile_data["currency_symbol"] = currency_symbols.get(currency)

        # convert to series
        profile_data = profile_data.squeeze()

    else:
        print(f"Failed to fetch data for {ticker}: {response.status_code}")
        profile_data = []

    return profile_data


get_profile_data(ticker="AAPL")
