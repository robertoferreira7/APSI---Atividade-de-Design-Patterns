from django.urls import path
from .views import select_strategy, calculate

urlpatterns = [
    path("select", select_strategy),
    path("calculate", calculate),
]
