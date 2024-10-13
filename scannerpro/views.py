from django.shortcuts import render

# Create your views here.
def scanner_home(request):
    return render(request, "scannerpro/home.html", {})