from datetime import timezone, datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

from transactions.models import Wallet

currency_choice = [("GBP", "GBP"), ("USD", "USD"), ("EUR", "EUR")]


# 4 usages
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    balance = forms.IntegerField(initial=1000)
    currency = forms.ChoiceField(choices=currency_choice, required=True)

    class Meta:
        model = User
        fields = ("username", "balance", "email", "password1", "password2", "currency")

    def save(self, *args, **kwargs):
        instance = super(RegisterForm, self).save(*args, **kwargs)
        Wallet.objects.create(user=instance, balance=self.cleaned_data['balance'])
        return instance


class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    balance = forms.IntegerField(initial=1000)
    currency = forms.ChoiceField(choices=currency_choice, required=True)
    is_admin = forms.BooleanField(label='Admin', required=True)

    class Meta:
        model = User
        fields = ("username", "balance", "email", "password1", "password2", "currency", "is_admin")

    def save(self, *args, **kwargs):
        instance = super(AdminRegistrationForm, self).save(*args, **kwargs)
        Wallet.objects.create(user=instance, balance=self.cleaned_data['balance'])
        return instance
