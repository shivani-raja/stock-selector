import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
from raw.get_ticker_data import get_ticker_data
from raw.get_market_data import get_market_data
import pandas as pd
import statistics

ticker = "AAPL"

data = get_ticker_data(ticker)


price_data = pd.read_json(data["price_data"], orient="split")
market_data = get_market_data()


def calculate_percentage_change(df):
    df = df.sort_values("date")
    start_price = df["adjClose"].iloc[0]
    df["rolling_change"] = (df["adjClose"] - start_price) / start_price * 100
    return df


# trim price data based on available market data
min_date = market_data["Date"].min()
price_data = price_data.loc[price_data["date"] >= min_date]

# make col names the same
market_data = market_data.rename(columns={'Date': 'date', 'Adj Close': 'adjClose', 'return': 'changePercent'})

# calculate % change
price_data = calculate_percentage_change(price_data)
market_data = calculate_percentage_change(market_data)

# merge data
returns = pd.merge(price_data, market_data, on='date', suffixes=(f"_{ticker}", '_SP500'))

# for beta calcs we use month end values
# fill nas
returns_dated = returns.set_index('date')
month_end_data = returns_dated.resample('BM').last()

# get monthly returns
month_end_data['monthly_return_SP500'] = month_end_data['adjClose_SP500'].pct_change() * 100
month_end_data[f'monthly_return_{ticker}'] = month_end_data[f'adjClose_{ticker}'].pct_change() * 100

# fill nas
month_end_data['monthly_return_SP500'] = month_end_data['monthly_return_SP500'].fillna(0)
month_end_data[f'monthly_return_{ticker}'] = month_end_data[f'monthly_return_{ticker}'].fillna(0)

# calculate beta, stddev + alpha
X = np.array(month_end_data['monthly_return_SP500']).reshape(-1, 1)
y = np.array(month_end_data[f"monthly_return_{ticker}"])


# calculate beta, alpha + stddev
model = LinearRegression()
model.fit(X,y)
beta = model.coef_
alpha = model.intercept_
stddev = statistics.stdev(y)


price_change_chart = go.Figure(
        go.Scatter(
            x=price_data["date"],
            y=price_data["change"],
            mode="lines",
            line=dict(color="#000", width=2),
            name="AAPL",
            hovertemplate="%{y:.2f}%",
        )
    )

price_change_chart.show()
