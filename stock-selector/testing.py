import plotly.graph_objects as go
from raw.get_ticker_data import get_ticker_data
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

ticker = "AAPL"

data = get_ticker_data(ticker)

cashflow_data = pd.read_json(data["cashflow_data"], orient="split")
price_data = pd.read_json(data["price_data"], orient="split")

output = pd.DataFrame(columns=["year","return"])

today = datetime.today()

output["year"] = [1,2,3,4,5]
for year in output["year"]:
    upper_date_bound = today - timedelta(days=(year-1)*365)
    lower_date_bound = today - timedelta(days=year*365)

    mask = price_data.loc[(price_data["date"]<upper_date_bound)&(price_data["date"]>=lower_date_bound)]

    # extract returns
    returns = np.array(mask["changeOverTime"])

    # add 1 to each return
    returns = returns + 1

    cumulative_product = np.prod(returns)

    # annualise return based on 252 trading days
    annualised_return = (cumulative_product ** (252 / len(returns))) - 1

    output.loc[output["year"]==year, "return"] = annualised_return

fig = go.Figure()