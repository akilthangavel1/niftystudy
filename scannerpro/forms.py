# forms.py
from django import forms
from .models import TickerBase

class TickerForm(forms.ModelForm):
    class Meta:
        model = TickerBase
        fields = ['ticker_name', 'ticker_symbol', 'ticker_sector', 'ticker_sub_sector', 'ticker_market_cap']
