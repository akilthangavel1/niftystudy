from django.shortcuts import render
import time
from django.http import StreamingHttpResponse


def scanner_home(request):
    return render(request, "scannerpro/home.html", {})


def generate_event_stream():
    while True:
        ticker_list = []  
        try:
            print("Fetching data...")  
            
            ticker_list = ["AAPL", "GOOGL", "TSLA"]  
            
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
        
        if ticker_list:
            for ticker in ticker_list:
                yield f"data: {ticker}\n\n"  # Yield ticker data one by one
        else:
            yield f"data: No data available\n\n"
        
        
        time.sleep(20)


def sse_event_view(request):
    response = StreamingHttpResponse(generate_event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

