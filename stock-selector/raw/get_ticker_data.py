import requests
import pandas as pd
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
    api_key = "52a44d5f713429851c9f7961317e6877"

    # define dictionary to store urls
    url_dict = {
        "profile_data": f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={api_key}",
        "income_statement_data": f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=annual&apikey={api_key}",
        "cashflow_data": f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period=annual&apikey={api_key}",
        "price_data": f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from=1990-10-10&apikey={api_key}",
    }

    required_data = [
        "profile_data",
        "income_statement_data",
        "cashflow_data",
        "price_data",
    ]
    output_data = {}

    for table in required_data:
        url = url_dict.get(table)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if table == "price_data":
                data = data.get("historical", [])

            # parse JSON
            df = pd.json_normalize(data)

            # amend data types
            if table == "income_statement_data":
                df["calendarYear"] = df["calendarYear"].astype(int)
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
            output_data[table] = df.to_json(orient="split")

        else:
            print(f"failed to fetch {table} for {ticker}: {response.status_code}")

    # get sankey data + append
    income_statement_data = pd.read_json(
        output_data["income_statement_data"], orient="split"
    )
    sankey_nodes, sankey_links = get_sankey_data(income_statement_data)

    output_data["sankey_nodes"] = sankey_nodes.to_json(orient="split")
    output_data["sankey_links"] = sankey_links.to_json(orient="split")

    return output_data
