from django.urls import path
from .views import HomePageView, podcast_info_view

urlpatterns = [
    path("", HomePageView.as_view(), name = "homepage"),
    path("podcast/<int:podcast_id>", podcast_info_view, name="podcast_info")
]