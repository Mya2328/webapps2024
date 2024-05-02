from django.urls import path
from .views import CurrencyConversionAPIView

urlpatterns = [
    path('<str:from_currency>/<str:to_currency>/<str:amount>/', CurrencyConversionAPIView.as_view(), name='currency-conversion'),
]