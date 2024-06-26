from sqlite3 import OperationalError
from django.contrib import messages

from django import forms
from . import models
import thriftpy2
from thriftpy2.rpc import make_client
timestamp_thrift = thriftpy2.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService
from datetime import datetime



# from django.contrib.auth.models import User

class CashTransferForm(forms.ModelForm):
    transaction_type = forms.CharField(widget=forms.HiddenInput(), initial='CR')

    class Meta:
        model = models.WalletTransaction
        fields = ["sender", "recipient", "amount", "transaction_type"]

        def clean(self):
            cleaned_data = super().clean()
            sender_username = cleaned_data.get("sender")
            amount_to_transfer = cleaned_data.get("amount")
            src_wallet = models.Wallet.objects.get(user__username=sender_username)
            if src_wallet.balance < amount_to_transfer:
                raise forms.ValidationError("Sender does not have enough funds to transfer.")
            return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sender'] = forms.CharField(widget=forms.HiddenInput(), initial=self.initial.get('sender'))


class FundRequestForm(forms.ModelForm):
    class Meta:
        model = models.FundRequest
        fields = ['fund_sender', 'amount', 'currency', 'fund_requester']
        widgets = {
            'fund_requester': forms.HiddenInput(),
            'currency': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FundRequestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        fund_request = super(FundRequestForm, self).save(commit=False)
        fund_request.fund_requester = self.request.user
        try:
            client = make_client(Timestamp, '127.0.0.1', 9090)
            timestamp = datetime.fromtimestamp(int(str(client.getCurrentTimestamp())))
            fund_request.created_at = timestamp
        except OperationalError:
            messages.info(self, f"Transfer operation is not possible now.")
        if commit:
            fund_request.save()
        return fund_request
