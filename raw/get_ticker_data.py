import os
import requests
import pandas as pd
from dotenv import load_dotenv

from raw.currency_symbols import get_currency_symbol
from raw.get_sankey_data import get_sankey_data


def get_ticker_data(ticker):
    """retrieves ticker data from financial modelling prep API

    :return:
        profile_data: company information
        income_statement_data: income statement data
        cashflow_data: cashflow statement data
        price_data: historical share price
    """

    # api key
    load_dotenv()
    api_key = os.getenv("FMP_API_KEY")

    # define dictionary to store urls
    url_dict = {
        "profile_data": f"https://financialmodelingprep.com/stable/profile/?symbol={ticker}&apikey={api_key}",
        "income_statement_data": f"https://financialmodelingprep.com/stable/income-statement/?symbol={ticker}&period=annual&apikey={api_key}",
        "cashflow_data": f"https://financialmodelingprep.com/stable/cash-flow-statement/?symbol={ticker}&period=annual&apikey={api_key}",
        "price_data": f"https://financialmodelingprep.com/stable/historical-price-eod/full?symbol={ticker}&from=1990-10-10&apikey={api_key}",
    }

    required_data = [
        "profile_data",
        "income_statement_data",
        "cashflow_data",
        "price_data",
    ]
    output_data = {}
    error_message = []

    for table in required_data:
        url = url_dict.get(table)
        response = requests.get(url)
        if response.status_code == 429:
            error_message.append(
                f"Max API calls reached. Please try again later.")
        elif response.status_code == 200:
            data = response.json()

            if data:
                # parse JSON
                df = pd.json_normalize(data)

                # amend data types
                if table in ["income_statement_data", "cashflow_data"]:
                    df["fiscalYear"] = df["fiscalYear"].astype(int)
                elif table == "price_data":
                    df["date"] = pd.to_datetime(df["date"])

                # get currency
                if table != "price_data":
                    try:
                        currency = df["reportedCurrency"].values[0]
                        df["currency_symbol"] = get_currency_symbol(currency)
                    except KeyError:
                        currency = df["currency"].values[0]
                        df["currency_symbol"] = get_currency_symbol(currency)

                # append to output
                output_data[table] = df.to_dict(orient="records")
            else:
                error_message.append(
                    f"Failed to fetch data for {ticker.upper()}. Please enter a valid ticker symbol."
                )
        else:
            error_message.append(f"Error {response.status_code} incurred for {ticker.upper()}.")

    if error_message:
        error_message = error_message[0]
        output_data = []
    else:
        # get sankey data + append
        income_statement_data = pd.DataFrame(output_data["income_statement_data"])
        sankey_nodes, sankey_links = get_sankey_data(income_statement_data)

        output_data["sankey_nodes"] = sankey_nodes.to_dict(orient="records")
        output_data["sankey_links"] = sankey_links.to_dict(orient="records")

    return output_data, error_message
