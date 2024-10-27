# scannerpro/management/commands/start_fyers_socket.py
from django.core.management.base import BaseCommand
from fyers_apiv3.FyersWebsocket import data_ws
from scannerpro.tasks import process_stock_data
from scannerpro.models import TickerBase


class Command(BaseCommand):
    help = 'Start Fyers WebSocket connection and listen for real-time data'

    def handle(self, *args, **kwargs):
        def onmessage(message):
            print(message)
            process_stock_data.delay(message)

        def onerror(message):
            print("Error:", message)

        def onclose(message):
            print("Connection closed:", message)

        def onopen():
            data_type = "SymbolUpdate"
            symbols = list(TickerBase.objects.values_list('ticker_symbol', flat=True))
            fyers_symbols = ["NSE:" + stock + "-EQ" for stock in symbols]
            print(fyers_symbols)
            fyers.subscribe(symbols=fyers_symbols, data_type=data_type)
            fyers.keep_running()

        access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3Mjk4MjM5ODgsImV4cCI6MTcyOTkwMjY0OCwibmJmIjoxNzI5ODIzOTg4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbkd3VDBMdFFqMnN5Y3Y4cVhNTUR5RUtJUlU0d1haN2JCeDNGQzdjNWpDRnk0bUh2eG9DZHIzREtPcGNmdi1vZi1Qalhjd2o0TDFrNVZ1eENreFVKeXEtSEhwdm1xWkFmQmpTUXduek1MSVpfYzRGTT0iLCJkaXNwbGF5X25hbWUiOiJBS0lMIFRIQU5HQVZFTCIsIm9tcyI6IksxIiwiaHNtX2tleSI6ImJlY2M0NDU4NmZjN2MyOTFhMWZjYTAwZmVjMjA2YmQ0MjNiOThlZDRiYWY4Mjc3YjZhMWI5Y2U2IiwiZnlfaWQiOiJZQTI5Mzk2IiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.JDE1es-xp8Am43EFP-WLrTpVtQd0iJSGazTWcJSFKnM"
        fyers = data_ws.FyersDataSocket(
            access_token=access_token,
            log_path="",
            litemode=False,
            write_to_file=False,
            reconnect=True,
            on_connect=onopen,
            on_close=onclose,
            on_error=onerror,
            on_message=onmessage
        )
        fyers.connect()
