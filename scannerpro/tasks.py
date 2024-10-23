# scannerpro/tasks.py
from celery import shared_task
import json
from .models import StockData

@shared_task
def process_stock_data(message):
    try:
        # Parse the message (assuming it's in JSON format)
        data = (message)
        # Extract the symbol and LTP (Latest Trading Price)
        symbol = data.get('symbol')
        ltp = data.get('ltp')
        # Store the data in the database
        if symbol and ltp:
            StockData.objects.create(symbol=symbol, ltp=ltp)

    except Exception as e:
        print(f"Error processing message: {e}")
