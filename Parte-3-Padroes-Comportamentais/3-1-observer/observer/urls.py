from django.urls import path
from .views import subscribe, unsubscribe, price
urlpatterns = [
    path("subscribe", subscribe),
    path("unsubscribe", unsubscribe),
    path("price", price),
]
