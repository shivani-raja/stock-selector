from domain.get_market_data import get_market_data
from domain.get_sankey_data import get_sankey_data

ticker = "AAPL"

ticker_data = get_market_data(ticker)

sankey_data = get_sankey_data(ticker_data)