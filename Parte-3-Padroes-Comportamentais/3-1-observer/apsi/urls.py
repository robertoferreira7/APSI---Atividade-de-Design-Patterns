from django.urls import path, include
urlpatterns = [
    path("api/observer/", include("observer.urls")),
]
