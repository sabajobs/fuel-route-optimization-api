from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def health_check(request):
    return JsonResponse({"status": "ok", "service": "fuel-route-api"})


urlpatterns = [
    path("", health_check),          # simple sanity endpoint
    path("admin/", admin.site.urls),
    path("api/", include("routing.urls")),
]
