import requests
import pandas as pd


def get_price_data(ticker):
    """gets historical share price data from financial modelling prep API

    :return: price_data, a dataset of historical share price
    """

    # api key
    api_key = "52a44d5f713429851c9f7961317e6877"

    # get data
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        historical_data = data.get('historical', [])
        price_data = pd.json_normalize(historical_data)

        # convert date to datetime
        price_data["date"] = pd.to_datetime(price_data["date"])

    else:
        print(f"Failed to fetch data for {ticker}: {response.status_code}")
        price_data = []

    return price_data