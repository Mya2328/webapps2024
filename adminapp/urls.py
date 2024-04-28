from django.urls import path
from . import views

app_name= 'adminapp'

urlpatterns = [
    path('', views.view_accounts, name='view_accounts'),
    path('add_admin/', views.add_admin, name='add_admin'),
    path('register/', views.view_register, name='view_register'),

]
