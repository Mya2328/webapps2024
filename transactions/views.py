from datetime import datetime

from django.db import transaction, OperationalError
from django.shortcuts import render, redirect, get_object_or_404

from conversion.views import CurrencyConversionAPIView
from notifications.models import Notification
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CashTransferForm
from django.db.models import Q

from .models import User, Wallet, WalletTransaction
from .models import FundRequest
from .forms import FundRequestForm
import thriftpy2
from thriftpy2.rpc import make_client

timestamp_thrift = thriftpy2.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


# Create your views here.
@login_required(login_url='login')
@csrf_protect
def transfer(request):
    src_wallet = None  # Initialize the variable to None
    if request.method == 'POST':
        form = CashTransferForm(request.POST,
                                initial={'sender': request.user.username})  # pass the sender value as initial
        if form.is_valid():
            src_username = form.cleaned_data["sender"]
            dst_username = form.cleaned_data["recipient"]
            amount_to_transfer = form.cleaned_data["amount"]

            # We use the select_for_update inside a transaction block to fetch the queryset to lock it until the transaction is completed.
            src_wallet = Wallet.objects.select_related().get(user__username=src_username)
            dst_wallet = Wallet.objects.select_related().get(user__username=dst_username)

            if not request.user.is_superuser and request.user.id != src_wallet.user.id:
                messages.error(request, "You can only transfer funds from your own account.")
                return redirect("transfer")

            if src_username == dst_username:
                messages.error(request, "You can only transfer funds to other account.")
                return redirect("transfer")

            if src_wallet.balance < amount_to_transfer:
                messages.error(request, "Insufficient funds.")
                return redirect("transfer")

            if src_wallet.currency != dst_wallet.currency:
                converted_amount = CurrencyConversionAPIView().get(request, src_wallet.currency, dst_wallet.currency,
                                                                   amount_to_transfer)
                if isinstance(converted_amount, dict) and 'converted_amount' in converted_amount:
                    converted_amount = converted_amount['converted_amount']
                else:
                    # Handle the case when the conversion fails
                    messages.error(request, "Currency conversion failed.")
                    return redirect("transfer")
            else:
                converted_amount = amount_to_transfer

            try:
                client = make_client(Timestamp, '127.0.0.1', 9090)  # Change settings.Timestamp to actual import path
                timestamp = datetime.fromtimestamp(int(str(client.getCurrentTimestamp())))
                with transaction.atomic():
                    src_wallet.balance -= amount_to_transfer
                    src_wallet.save()
                    print(amount_to_transfer)
                    dst_wallet.balance += converted_amount
                    dst_wallet.save()
                    print(converted_amount)

                    if src_username == request.user.username:
                        transaction_type = 'DR'
                        recipient_transaction_type = 'CR'
                    else:
                        transaction_type = 'CR'
                        recipient_transaction_type = 'DR'

                    # Create and save a new WalletTransaction object for the sender
                    src_transaction = WalletTransaction.objects.create(
                        sender=src_username,
                        recipient=dst_username,
                        amount=amount_to_transfer,
                        transaction_type=transaction_type,
                        date_created=timestamp,
                    )

                    # Create and save a new WalletTransaction object for the recipient
                    dst_transaction = WalletTransaction.objects.create(
                        sender=src_username,
                        recipient=dst_username,
                        amount=converted_amount,
                        transaction_type=recipient_transaction_type,
                        date_created=timestamp,
                    )

                @transaction.on_commit
                def send_transfer_message():
                    messages.success(request,
                                     f"{amount_to_transfer} {src_wallet.currency} have been transferred from {src_username} to {dst_username}.")

            except OperationalError:
                messages.info(request, f"Transfer operation is not possible now.")

        src_transactions = list(
            WalletTransaction.objects.filter(sender=request.user.username).order_by("-date_created"))
        dst_transactions = list(
            WalletTransaction.objects.filter(recipient=request.user.username).order_by("-date_created"))

        context = {
            "src_wallet": src_wallet,
            "src_transactions": src_transactions,
            "src_transaction_amount": src_transaction.amount if 'src_transaction' in locals() else None,
            "src_transaction_date": src_transaction.date_created if 'src_transaction' in locals() else None,
            "src_transaction_type": src_transaction.transaction_type if 'src_transaction' in locals() else None,
            "src_sender_balance": src_wallet.balance if src_wallet else None,
            "dst_transactions": dst_transactions,
            "dst_username": dst_username,
        }
        return render(request, "transactions/account_details.html", context)

    else:
        form = CashTransferForm(initial={'sender': request.user.username})
    return render(request, "transactions/transfer.html", {"form": form})

@login_required(login_url='login')
def transactionlog(request):
    # Fetch all transactions for the source wallet
    src_transactions = list(
        WalletTransaction.objects.filter(sender=request.user.username, recipient__isnull=False).order_by(
            "-date_created"))

    # Fetch all transactions for the destination wallet
    dst_transactions = list(WalletTransaction.objects.filter(recipient=request.user.username).order_by("-date_created"))

    # Fetch all fund requests sent by the user
    fund_requests_sent = list(FundRequest.objects.filter(fund_sender=request.user).order_by("-created_at"))

    # Fetch all fund requests received by the user excluding ones they sent
    fund_requests_received = list(FundRequest.objects.filter(fund_requester=request.user).exclude(
        Q(fund_sender=request.user) | Q(fund_sender=None)).order_by("-created_at"))

    # Merge transactions and fund requests into a single list and sort them by date_created or created_at in descending order
    transactions = sorted(
        src_transactions + dst_transactions + fund_requests_sent + fund_requests_received,
        key=lambda x: x.date_created if hasattr(x, 'date_created') else x.created_at,
        reverse=True
    )

    rate = {'USD': 1.24, 'EUR': 1.16, 'GBP': 1.00}
    context = {
        'transactions': transactions,
        'rate': rate
    }
    return render(request, 'transactions/transactionlog.html', context)


def send_and_request(request):
    return render(request, "payapp/send&request.html")


@login_required(login_url='login')
def requestmoney(request):
    if request.method == 'POST':
        form = FundRequestForm(request.POST, request=request)
        if form.is_valid():
            fund_request = form.save()
            fund_request.fund_requester = request.user
            # Set the currency to the user's currency from their Wallet
            wallet = Wallet.objects.get(user=request.user)
            fund_request.currency = wallet.currency
            fund_request.save()
            messages.success(request, 'Your fund request has been sent.')
            return redirect('fund_request_list')
    else:
        fund_requester = request.user
        # print(fund_requester) # add this line to check the value of fund_requester
        form = FundRequestForm(initial={'fund_requester': fund_requester})
        form.fields['fund_sender'].queryset = User.objects.exclude(pk=fund_requester.pk)
    return render(request, 'transactions/requestmoney.html', {'form': form})


def fund_request_list(request):
    pending_requests = FundRequest.objects.filter(fund_sender=request.user, status='PENDING')
    return render(request, 'transactions/fund_request_list.html', {'pending_requests': pending_requests})


def fund_request_action(request, pk):
    request_obj = get_object_or_404(FundRequest, pk=pk)
    fund_requester = request_obj.fund_requester
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            request_obj.approve()
            messages.success(request, 'The fund request has been approved.')
            notify = f"Your Fund request of{request_obj.amount}{request_obj.currency} was approved by{request_obj.fund_sender}"
            Notification.send_notification(fund_requester, notify)
        elif action == 'decline':
            request_obj.decline()
            messages.error(request, 'The fund request has been declined.')
        return redirect('fund_request_list')

    return render(request, 'transactions/fund_request_action.html', {'request': request_obj})
