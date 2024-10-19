
# import yfinance as yf
# import pandas as pd

# # Define the ticker symbols for the indices
# index_tickers = {
#     'S&P 500': '^GSPC',
#     'NASDAQ': '^IXIC',
#     'DOW JONES': '^DJI',
#     'FTSE 100': '^FTSE',
#     'NIFTY 50': '^NSEI'
# }

# # Function to fetch historical data for an index
# def get_index_data(ticker, period='1y', interval='1d'):
#     index_data = yf.download(ticker, period=period, interval=interval)
#     return index_data

# # Loop through each index and fetch data
# index_data = {}
# for index_name, ticker in index_tickers.items():
#     print(f"Fetching data for {index_name}...")
#     data = get_index_data(ticker, period='1y', interval='1d')  # Example: last 1 year of daily data
#     index_data[index_name] = data

# # Example: Print the head of each index data
# for index_name, data in index_data.items():
#     print(f"\nData for {index_name}:")
#     print(data.head())

# # Example: Save each index data to a CSV file
# for index_name, data in index_data.items():
#     data.to_csv(f"{index_name}_data.csv")
#     print(f"{index_name} data saved to {index_name}_data.csv")

