from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.view_accounts, name='view_accounts'),
    path('add_admin/', views.add_admin, name='add_admin'),
]
