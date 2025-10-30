# payment_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/pay/', views.process_payment, name='process_payment'),
]