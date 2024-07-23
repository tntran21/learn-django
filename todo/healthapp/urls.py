from django.urls import path
from healthapp.views import HealthViews

urlpatterns = [
    path("", HealthViews.get_data, name="health"),
    path("create", HealthViews.post_data, name="post_health"),
    path("update/<int:pk>", HealthViews.update_data, name="update_health"),
]
