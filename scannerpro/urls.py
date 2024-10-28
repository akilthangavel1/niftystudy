from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.scanner_home, name='scanner_home'),  # Home page
    path('scannertest/', views.scanner_test, name='scanner_test'), 
    path('sse_event/', views.sse_event_view, name='sse_event'),  # SSE endpoint
    path('sse-index/', views.index_sse_event_view, name='index-sse'),
    path('tickers/', views.ticker_list, name='ticker-list'),  # Read all
    path('tickers/<int:pk>/', views.ticker_detail, name='ticker-detail'),  # Read single
    path('tickers/create/', views.ticker_create, name='ticker-create'),  # Create
    path('tickers/<int:pk>/update/', views.ticker_update, name='ticker-update'),  # Update
    path('tickers/<int:pk>/delete/', views.ticker_delete, name='ticker-delete'),  # Delete
]
