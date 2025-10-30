from django.urls import path, include

urlpatterns = [
    path("api/strategy/", include("strategy.urls")),
]
