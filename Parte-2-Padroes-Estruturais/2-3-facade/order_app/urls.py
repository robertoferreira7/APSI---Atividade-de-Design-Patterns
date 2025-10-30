# order_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/order/place/', views.place_order_api, name='place_order'),
]