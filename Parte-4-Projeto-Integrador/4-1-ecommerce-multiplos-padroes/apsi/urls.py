from django.urls import path, include

urlpatterns = [
    path("api/integrator/", include("integrator.urls")),
]
