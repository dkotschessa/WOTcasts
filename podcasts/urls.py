from django.urls import path
from .views import homepage_view, podcast_info_view, podcast_gallery_view

urlpatterns = [
    path("", homepage_view, name = "homepage"),
    path('podcasts', podcast_gallery_view, name="podcast_gallery"),
    path("podcast/<int:podcast_id>", podcast_info_view, name="podcast_info")
]