
#imports 
from fyers_apiv3 import fyersModel
import time
from datetime import datetime
import pandas as pd


def date_to_timestamp(date_str, date_format="%d/%m/%Y"):
    dt = datetime.strptime(date_str, date_format)
    return int(time.mktime(dt.timetuple()))

def fetch_ohlc_data(symbol, resolution, from_date, to_date, client_id, access_token, date_format="%d/%m/%Y"):
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
    range_from = date_to_timestamp(from_date, date_format)
    range_to = date_to_timestamp(to_date, date_format) + 24 * 60 * 60  
    data = {
        "symbol": symbol,
        "resolution": resolution,        
        "date_format": "0",              
        "range_from": str(range_from),   
        "range_to": str(range_to),       
        "cont_flag": "1"                
    }
    try:
        response = fyers.history(data=data)
        if response.get('s') == 'ok':
            return response
        else:
            return f"Error in response: {response}"
    except Exception as e:
        return f"An error occurred: {e}"


def process_ohlc_data(response):
    if 'candles' not in response:
        return "No candle data found in response."
    candles = response['candles']
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    
    return df


def get_data():
    pass