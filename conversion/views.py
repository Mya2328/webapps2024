from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal

class CurrencyConversionAPIView(APIView):
    def get_exchange_rate(self, from_currency, to_currency):
        exchange_rates = {
            "GBP": {"EUR": Decimal("1.13"), "USD": Decimal("1.25"), "GBP":Decimal("1.00")},
            "USD": {"EUR": Decimal("0.91"), "GBP": Decimal("0.80"), "USD":Decimal("1.00")},
            "EUR": {"GBP": Decimal("0.89"), "USD": Decimal("1.10"), "EUR":Decimal("1.00")},
        }
        return exchange_rates.get(from_currency, {}).get(to_currency)

    def get(self, request, from_currency, to_currency, amount):
        exchange_rate = self.get_exchange_rate(from_currency.upper(), to_currency.upper())
        print('This is exchange rates', exchange_rate)
        if exchange_rate is None:
            return Response({"error": "Invalid currency pair"}, status=status.HTTP_404_NOT_FOUND )

        try:
            amount = Decimal(amount)
        except ValueError:
            return Response({"error": "Invalid amount"}, status=status.HTTP_404_NOT_FOUND )

        converted_amount = amount * exchange_rate
        print('This is converted_amount', converted_amount)
        return Response({'converted_amount': converted_amount}, status=status.HTTP_200_OK)