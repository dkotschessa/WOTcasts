from django.urls import path
from .views import (
    # homepage_view,
    HomepageView,
    youtube_episodes_view,
    channel_info_view,
    PodcastInfoView,
    PodcastGalleryView,
    PodcastSearchResultsView,
    AboutView,
    youtube_gallery_view,
    youtube_search_results_view,
    get_content_by_date_view,
    get_content_by_date_range_view,
)

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path(
        "content_by_date/<str:content_date>",
        get_content_by_date_view,
        name="content_by_date",
    ),
    path(
        "content_by_date_range/<str:start_date>/<str:end_date>",
        get_content_by_date_range_view,
        name="content_by_date_range",
    ),
    path("wheel_of_youtube", youtube_episodes_view, name="youtube_episodes"),
    path("youtube_channels", youtube_gallery_view, name="youtube_gallery"),
    path(
        "podcasts/channels/<int:channel_id>",
        channel_info_view,
        name="youtube_channel_info",
    ),
    path("podcasts", PodcastGalleryView.as_view(), name="podcast_gallery"),
    path("about", AboutView.as_view(), name="about"),
    path("podcast/<int:podcast_id>", PodcastInfoView.as_view(), name="podcast_info"),
    path("search_results", PodcastSearchResultsView.as_view(), name="search_results"),
    path(
        "youtube_search_results",
        youtube_search_results_view,
        name="youtube_search_results",
    ),
]
