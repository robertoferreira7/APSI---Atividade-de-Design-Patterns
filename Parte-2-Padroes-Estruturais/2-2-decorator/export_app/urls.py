# export_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/export/', views.export_data, name='export_data'),
]