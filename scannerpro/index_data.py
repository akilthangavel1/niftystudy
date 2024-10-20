
import yfinance as yf
import pandas as pd

index_tickers = {
    'S&P 500': '^GSPC',
    'NASDAQ': '^IXIC',
    'DOW JONES': '^DJI',
    'FTSE 100': '^FTSE',
    'NIFTY 50': '^NSEI'
}

index_data = yf.download( '^GSPC', period='1y', interval='1d')
print(index_data)