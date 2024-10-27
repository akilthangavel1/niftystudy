import yfinance as yf
import pandas as pd



def fetch_index_data(ticker):
    try:
        index_data = yf.download(ticker, period='1y', interval='1d')
        # print(index_data)
        # print("###########################################")
        if not index_data.empty:
            index_data = index_data[['Open', 'High', 'Low', 'Close', 'Volume']]
            index_data['Date'] = index_data.index
            index_data.reset_index(drop=True, inplace=True)
            return index_data
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None
