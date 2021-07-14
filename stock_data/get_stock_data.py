import datetime

import yfinance as yf
import matplotlib.pyplot as plt

# store ticker values for AMD, Disney, and Tesla
tickers = ('AMD', 'DIS', 'TSLA')

# get all ticker data for Microsoft
ticker_data = yf.Ticker('MSFT')

# get close prices for tickers
stock_prices = yf.download(tickers, start="2020-1-1", end=datetime.datetime.now().strftime('%Y-%m-%d'), peroid='ytd').Close

#print(stock_prices)
#print(ticker_data.history(period='1d', start='2020-1-1', end=datetime.datetime.now().strftime('%Y-%m-%d')))


stock_prices['AMD'].plot()
stock_prices['DIS'].plot()
stock_prices['TSLA'].plot()
ticker_data.history(period='1d', start='2020-1-1', end=datetime.datetime.now().strftime('%Y-%m-%d')).Close.plot(
    label='MSFT')

plt.title('Stock Prices for AMD, Disney, and Tesla')
plt.ylabel('Stock Price')
plt.legend()
plt.show()
