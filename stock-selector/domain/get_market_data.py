import requests
import pandas as pd

# api key
api_key = "52a44d5f713429851c9f7961317e6877"

# get list of ticker symbols - for now we import top 50 market cap stocks as at 15/06/2024 from a csv file
# this is due to limitations in querying the API on free plan

ticker_data = pd.read_csv("ticker_symbols.csv")
ticker_list = ticker_data["Symbol"]

# create df to store results
financial_statements = pd.DataFrame()

# get data
for ticker in ticker_list:
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=annual&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        parsed_data = pd.json_normalize(data)
        financial_statements = pd.concat([financial_statements, parsed_data])
    else:
        print(f"Failed to fetch data: {response.status_code}")

print(financial_statements)
