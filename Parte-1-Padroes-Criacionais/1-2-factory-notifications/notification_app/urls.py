# notification_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('notify/', views.send_notification, name='send_notification'),
]