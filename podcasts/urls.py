from django.urls import path
from .views import (
    homepage_view,
    youtube_episodes_view,
    channel_info_view,
    podcast_info_view,
    podcast_gallery_view,
    podcast_search_results_view,
    about_view,
    youtube_gallery_view,
    youtube_search_results_view,
)

urlpatterns = [
    path("", homepage_view, name="homepage"),
    path("wheel_of_youtube", youtube_episodes_view, name="youtube_episodes"),
    path("youtube_channels", youtube_gallery_view, name="youtube_gallery"),
    path(
        "podcasts/channels/<int:channel_id>",
        channel_info_view,
        name="youtube_channel_info",
    ),
    path("podcasts", podcast_gallery_view, name="podcast_gallery"),
    path("about", about_view, name="about"),
    path("podcast/<int:podcast_id>", podcast_info_view, name="podcast_info"),
    path("search_results", podcast_search_results_view, name="search_results"),
    path(
        "youtube_search_results",
        youtube_search_results_view,
        name="youtube_search_results",
    ),
]
