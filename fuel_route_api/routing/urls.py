from django.urls import path
from .views import RouteAPIView

# API endpoints for routing service
urlpatterns = [
    path("route/", RouteAPIView.as_view(), name="route"),
]
