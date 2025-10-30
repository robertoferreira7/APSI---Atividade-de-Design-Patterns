from django.urls import path, include

urlpatterns = [
    path("api/template/", include("template_method.urls")),
]
