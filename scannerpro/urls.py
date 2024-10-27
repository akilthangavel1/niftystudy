from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.scanner_home, name='scanner_home'),  # Home page
    path('scannertest/', views.scanner_test, name='scanner_test'), 
    path('sse_event/', views.sse_event_view, name='sse_event'),  # SSE endpoint
    path('sse-index/', views.index_sse_event_view, name='index-sse'),
]
