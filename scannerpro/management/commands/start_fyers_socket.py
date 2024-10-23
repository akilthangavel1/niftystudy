# scannerpro/management/commands/start_fyers_socket.py
from django.core.management.base import BaseCommand
from fyers_apiv3.FyersWebsocket import data_ws
from scannerpro.tasks import process_stock_data

class Command(BaseCommand):
    help = 'Start Fyers WebSocket connection and listen for real-time data'

    def handle(self, *args, **kwargs):
        def onmessage(message):
            print("#########################################")
            print(message)
            process_stock_data.delay(message)

        def onerror(message):
            print("Error:", message)

        def onclose(message):
            print("Connection closed:", message)

        def onopen():
            data_type = "SymbolUpdate"
            symbols = ["MCX:CRUDEOILM24NOVFUT"]
            fyers.subscribe(symbols=symbols, data_type=data_type)
            fyers.keep_running()

        access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3Mjk2Nzk4NTMsImV4cCI6MTcyOTcyOTgzMywibmJmIjoxNzI5Njc5ODUzLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbkdOSHQtcGtPRlp3WWFKZXNKUEdTQkhtbEswOUNNV3pPVU5NeTJFd1ZNNzB5Q3hiV1J4emZSb0l0c2prS2tZT0o1d3VPOHAyWVNMclgtcUh3dzJ0YUs5d2c5dlJMU2RrVkNXSXRqRDNoWnVwSUxlaz0iLCJkaXNwbGF5X25hbWUiOiJBS0lMIFRIQU5HQVZFTCIsIm9tcyI6IksxIiwiaHNtX2tleSI6ImJlY2M0NDU4NmZjN2MyOTFhMWZjYTAwZmVjMjA2YmQ0MjNiOThlZDRiYWY4Mjc3YjZhMWI5Y2U2IiwiZnlfaWQiOiJZQTI5Mzk2IiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.bZt2ojffpMtgYMe82dkDS41gi93ojREcv2YMWEm6co4"
        fyers = data_ws.FyersDataSocket(
            access_token=access_token,
            log_path="",
            litemode=True,
            write_to_file=False,
            reconnect=True,
            on_connect=onopen,
            on_close=onclose,
            on_error=onerror,
            on_message=onmessage
        )
        fyers.connect()
