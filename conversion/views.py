from rest_framework.views import APIView
from decimal import Decimal

class CurrencyConversionAPIView(APIView):
    def get_exchange_rate(self, from_currency, to_currency):
        exchange_rates = {
            "GBP": {"EUR": Decimal("1.13"), "USD": Decimal("1.25")},
            "USD": {"EUR": Decimal("0.91"), "GBP": Decimal("0.80")},
            "EUR": {"GBP": Decimal("0.89"), "USD": Decimal("1.10")},
        }
        return exchange_rates.get(from_currency, {}).get(to_currency)

    def get(self, request, from_currency, to_currency, amount):
        exchange_rate = self.get_exchange_rate(from_currency.upper(), to_currency.upper())
        if exchange_rate is None:
            return {"error": "Invalid currency pair"}

        try:
            amount = Decimal(amount)
        except ValueError:
            return {"error": "Invalid amount"}

        converted_amount = amount * exchange_rate
        return {'converted_amount': converted_amount}