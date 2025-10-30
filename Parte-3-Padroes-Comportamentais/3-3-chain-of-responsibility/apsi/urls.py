from django.urls import path, include

urlpatterns = [
    path("api/chain/", include("chain.urls")),
]
