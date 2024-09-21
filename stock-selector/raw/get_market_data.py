import yfinance as yf
from datetime import datetime, timedelta


def get_market_data():
    """retrieves market data from yahoo finance

    :return:
        market_data: historical S&P500 returns
    """

    # get today's date and 5y ago date
    end_date = datetime.today()
    start_date = end_date - timedelta(days=(5 * 365))

    # get data for S&P500 (^GSPC)
    market_data = yf.download('^GSPC', start=start_date, end=end_date)

    # remove index column
    market_data = market_data.reset_index()

    # calculate the daily returns
    market_data['return'] = market_data['Adj Close'].pct_change()

    return market_data