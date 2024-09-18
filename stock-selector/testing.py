import plotly.graph_objects as go
from raw.get_ticker_data import get_ticker_data

ticker = "AAPL"

all_data, currency = get_ticker_data(ticker)

year = 2023