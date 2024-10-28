from django.shortcuts import render
import time
from django.http import HttpResponse, StreamingHttpResponse
from scannerpro.tasks import process_stock_data
from .stock_data_history import fetch_ohlc_data, process_ohlc_data
from .models import TickerBase
import pandas as pd

client_id = "MMKQTWNJH3-100"
secret_key = "EUT312TGNM"
redirect_url = "http://localhost:4004/"
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MzAwODQ3NDUsImV4cCI6MTczMDE2MTg0NSwibmJmIjoxNzMwMDg0NzQ1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbkh2LUpxS1pfY0VNSGh6Tm1jWWNhSTZEQXJlcGJZX01faTVOVDB3Q2VsbC15UGMwNGZHdFh3cWo4UE9PbzA4V0FCMVpGS3A4NmRqSFpYNGdZaFFSdGFsbFV0MEpZaHVMa3l0VTZxa2Rzekx2d0RBMD0iLCJkaXNwbGF5X25hbWUiOiJBS0lMIFRIQU5HQVZFTCIsIm9tcyI6IksxIiwiaHNtX2tleSI6ImJlY2M0NDU4NmZjN2MyOTFhMWZjYTAwZmVjMjA2YmQ0MjNiOThlZDRiYWY4Mjc3YjZhMWI5Y2U2IiwiZnlfaWQiOiJZQTI5Mzk2IiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.mfP5xVfpKr7I1d649Ej0pfokE6HDShhDkWsM6uxWf1o'


def scanner_home(request):
    # symbols = list(TickerBase.objects.values_list('ticker_symbol', flat=True))
    # result_signals = {'ticker': [], 'datetime': [], 'Signal': []}
    # fyers_symbols = ["NSE:" + stock + "-EQ" for stock in symbols]
    # for i in fyers_symbols:
    #     try:
    #         df = fetch_ohlc_data(i, "D", "13/01/2024", "24/09/2024", client_id, access_token)
    #         df = process_ohlc_data(df) 
    #         df['SMABLUE'] = df['close'].rolling(window=10).mean()
    #         df['SMAYELLOW'] = df['close'].rolling(window=20).mean()
    #         df['Signal'] = 0
    #         df.loc[df['SMABLUE'] > df['SMAYELLOW'], 'Signal'] = 1
    #         df.loc[df['SMABLUE'] < df['SMAYELLOW'], 'Signal'] = -1
    #         signal_change = (df['Signal'].shift(1) != df['Signal'])
    #         last_change_index = df[signal_change].index[-1] if signal_change.any() else None
    #         if last_change_index:
    #             data_values = df.loc[last_change_index]
    #             print(data_values['datetime'], data_values['Signal'])
    #             result_signals['ticker'].append(i)
    #             result_signals['datetime'].append(data_values['datetime'])
    #             result_signals['Signal'].append(data_values['Signal'])
    #     except Exception as e:
    #         print(f"Error processing {i}: {str(e)}")            
    # result_signals = pd.DataFrame(result_signals)
    # print(result_signals)
    # return HttpResponse("Hello World!!!!")
    return render(request, "scannerpro/home.html", {})
    


def scanner_test(request):
    return render(request, "scannerpro/scn.html", {})


def generate_event_stream():
    while True:
        try:
            symbols = list(TickerBase.objects.values_list('ticker_symbol', flat=True))
            result_signals = {'ticker': [], 'datetime': [], 'Signal': []}
            fyers_symbols = ["NSE:" + stock + "-EQ" for stock in symbols]
            
            for i in fyers_symbols:
                try:
                    df = fetch_ohlc_data(i, "D", "13/01/2024", "24/09/2024", client_id, access_token)
                    
                    df = process_ohlc_data(df)
                    
                    if isinstance(df, dict):
                        df = pd.DataFrame(df)
                    if not isinstance(df, pd.DataFrame) or df.empty:
                        print(f"No valid data for {i}")
                        continue
                    
                    df['SMABLUE'] = df['close'].rolling(window=10).mean()
                    df['SMAYELLOW'] = df['close'].rolling(window=20).mean()
                    df['Signal'] = 0
                    df.loc[df['SMABLUE'] > df['SMAYELLOW'], 'Signal'] = 1
                    df.loc[df['SMABLUE'] < df['SMAYELLOW'], 'Signal'] = -1
                    
                    signal_change = (df['Signal'].shift(1) != df['Signal'])
                    last_change_index = df[signal_change].index[-1] if signal_change.any() else None
                    # print(df)
                    if last_change_index is not None:
                        data_values = df.loc[last_change_index]
                        result_signals['ticker'].append(i)
                        result_signals['datetime'].append(data_values['datetime'])
                        result_signals['Signal'].append(data_values['Signal'])
                except Exception as e:
                    print(f"Error processing {i}: {str(e)}")
            
            if result_signals['ticker']:
                # Create a DataFrame from result_signals
                result_signals_df = pd.DataFrame(result_signals)
                
                # Ensure the datetime column is treated as datetime type
                result_signals_df['datetime'] = pd.to_datetime(result_signals_df['datetime'])
                
                # Sort the DataFrame by datetime in descending order
                result_signals_df.sort_values(by='datetime', ascending=False, inplace=True)
                
                # Format the datetime column (e.g., "DD-MM-YYYY HH:MM:SS")
                result_signals_df['datetime'] = result_signals_df['datetime'].dt.strftime('%d-%m-%Y %H:%M:%S')
                
                # Convert to JSON and yield
                json_data = result_signals_df.to_json(orient='records')
                yield f"data: {json_data}\n\n"
            else:
                # Send an empty array if there are no signals
                yield "data: []\n\n"
            
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            yield f"data: Exception occurred: {str(e)}\n\n"
        
        # Sleep for a while before the next iteration
        time.sleep(200)


def sse_event_view(request):
    response = StreamingHttpResponse(generate_event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response



import time
import json
import logging
from django.http import StreamingHttpResponse
from .index_data_fn import fetch_index_data

logger = logging.getLogger(__name__)

# Define the index tickers
index_tickers = {
    'S&P 500': '^GSPC',
    'NASDAQ': '^IXIC',
    'DOW JONES': '^DJI',
    'FTSE 100': '^FTSE',
    'NIFTY 50': '^NSEI'
}

# def generate_index_event_stream():
#     while True:
#         index_results = []
#         for name, ticker in index_tickers.items():
#             try:
#                 # Fetch index data
#                 data = fetch_index_data(ticker)
#             except Exception as e:
#                 logger.error(f"Error fetching data for {ticker}: {e}")
#                 continue  # Skip this ticker and continue to the next

#             if data is not None and not data.empty:
#                 print(data)  # For debugging; consider using logging
#                 latest_data = data.iloc[-1]  # Get the latest row
#                 previous_data = data.iloc[-2] if len(data) > 1 else None  # Ensure there's a previous row

#                 if previous_data is not None and not previous_data.empty:
#                     previous_close = previous_data['Close'].iloc[0]  # Ensure this is a scalar
#                     latest_close = latest_data['Close'].iloc[0]  # Ensure this is a scalar
                    
#                     if previous_close != 0:  # Avoid division by zero
#                         percentage_change = ((latest_close - previous_close) / previous_close) * 100
#                     else:
#                         percentage_change = None  # Handle division by zero
#                 else:
#                     percentage_change = None  # Handle case where previous data is not available
                
#                 # Ensure that percentage_change is a float or None
#                 if percentage_change is not None:
#                     percentage_change = float(percentage_change)  # Ensure it's a float
                
#                 index_results.append({
#                     'Index Name': name,
#                     'Percentage Change': percentage_change  # Guaranteed to be a float or None
#                 })
#         print(index_results)
#         # Yield the results as JSON
#         if index_results:
#             json_data = json.dumps(index_results, default=str)  # Ensure proper serialization
#             yield f"data: {json_data}\n\n"
#         else:
#             yield "data: []\n\n"

#         time.sleep(300)  # Wait for 5 minutes before the next update


def generate_index_event_stream():
    while True:
        index_results = []
        for name, ticker in index_tickers.items():
            try:
                # Fetch index data
                data = fetch_index_data(ticker)
            except Exception as e:
                logger.error(f"Error fetching data for {ticker}: {e}")
                continue  # Skip this ticker and continue to the next

            if data is not None and not data.empty:
                print(data)  # For debugging; consider using logging
                latest_data = data.iloc[-1]  # Get the latest row
                previous_data = data.iloc[-2] if len(data) > 1 else None  # Ensure there's a previous row

                if previous_data is not None and not previous_data.empty:
                    previous_close = previous_data['Close'].iloc[0]  # Ensure this is a scalar
                    latest_close = latest_data['Close'].iloc[0]  # Ensure this is a scalar
                    
                    if previous_close != 0:  # Avoid division by zero
                        percentage_change = ((latest_close - previous_close) / previous_close) * 100
                    else:
                        percentage_change = None  # Handle division by zero
                else:
                    percentage_change = None  # Handle case where previous data is not available
                
                # Ensure that percentage_change is a float or None
                if percentage_change is not None:
                    percentage_change = round(float(percentage_change), 2)  # Round to 2 decimal places
                
                index_results.append({
                    'Index Name': name,
                    'Percentage Change': percentage_change  # Guaranteed to be a float or None
                })
        
        print(index_results)
        # Yield the results as JSON
        if index_results:
            json_data = json.dumps(index_results, default=str)  # Ensure proper serialization
            yield f"data: {json_data}\n\n"
        else:
            yield "data: []\n\n"

        time.sleep(300)  # Wait for 5 minutes before the next update

from django.shortcuts import render

def index_sse_event_view(request):
    response = StreamingHttpResponse(generate_index_event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import TickerBase
from .forms import TickerForm  # Importing a form for handling the TickerBase model
from django.http import HttpResponse


def ticker_list(request):
    tickers = TickerBase.objects.all()
    return render(request, 'scannerpro/ticker_list.html', {'tickers': tickers})


def ticker_detail(request, pk):
    ticker = get_object_or_404(TickerBase, pk=pk)
    return render(request, 'scannerpro/ticker_detail.html', {'ticker': ticker})


def ticker_create(request):
    if request.method == 'POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticker-list')
    else:
        form = TickerForm()
    return render(request, 'scannerpro/ticker_form.html', {'form': form})


def ticker_update(request, pk):
    ticker = get_object_or_404(TickerBase, pk=pk)
    if request.method == 'POST':
        form = TickerForm(request.POST, instance=ticker)
        if form.is_valid():
            form.save()
            return redirect('ticker-list')
    else:
        form = TickerForm(instance=ticker)
    return render(request, 'scannerpro/ticker_form.html', {'form': form})


def ticker_delete(request, pk):
    ticker = get_object_or_404(TickerBase, pk=pk)
    if request.method == 'POST':
        ticker.delete()
        return redirect('ticker-list')
    return render(request, 'scannerpro/ticker_confirm_delete.html', {'ticker': ticker})