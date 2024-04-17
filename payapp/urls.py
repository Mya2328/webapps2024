from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('summary/', views.summary, name="dashboard"),
    path('generate_plot/', views.generate_plot, name='generate_plot'),
]