from django.contrib import admin
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
# Import your models
from .models import Transaction, Account

# Import User model if not already imported
from django.contrib.auth.models import User

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp')
    # Customize any other settings or behaviors here

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    # Customize any other settings or behaviors here

# Register your models with their respective ModelAdmin classes
# admin.site.register(Transaction, TransactionAdmin)
# admin.site.register(Account, AccountAdmin)

# Define a view for adding admin users
class YourAdminUserForm:
    pass


def add_admin(request):
    # You may want to implement some logic here to ensure only superusers can access this view
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('register:login'))

    # Your logic for adding admin users goes here
    # For example:
    # if request.method == 'POST':
    #      form = YourAdminUserForm(request.POST)
    #      if form.is_valid():
    #          form.save()
    #          return HttpResponseRedirect(reverse('admin:index'))
    # else:
    #     form = YourAdminUserForm()

    return render(request, 'admin/add_admin.html')
    # return render(request, 'admin/add_admin.html')  # Placeholder until you implement the form

# Optionally, you can define other views related to admin operations here
def view_accounts():
    return None


