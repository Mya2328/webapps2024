from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@csrf_protect
def home(request):
    return render(request, "payapp/home.html")

@login_required(login_url='login')
def dashboard(request):
   return render(request, 'payapp/dashboard.html')

