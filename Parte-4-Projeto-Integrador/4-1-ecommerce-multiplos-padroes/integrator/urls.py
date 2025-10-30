from django.urls import path
from .views import product_create, subscribe, product_restock, cart_price, checkout

urlpatterns = [
    path("products/create", product_create),
    path("subscribe", subscribe),
    path("products/restock", product_restock),
    path("cart/price", cart_price),
    path("checkout", checkout),
]
