# logging_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('logs/', views.get_logs_view, name='get_logs'),
]