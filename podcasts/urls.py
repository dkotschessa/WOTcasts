from django.urls import path
from .views import (
    # homepage_view,
    HomepageView,
    YoutubeEpisodesView,
    ChannelInfoView,
    PodcastInfoView,
    PodcastGalleryView,
    PodcastSearchResultsView,
    AboutView,
    YoutubeGalleryView,
    YoutubeSearchResultsView,
    ContentByDateView,
    ContentByDateRangeView,
)

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path(
        "content_by_date/<str:content_date>",
        ContentByDateView.as_view(),
        name="content_by_date",
    ),
    path(
        "content_by_date_range/<str:start_date>/<str:end_date>",
        ContentByDateRangeView.as_view(),
        name="content_by_date_range",
    ),
    path("wheel_of_youtube", YoutubeEpisodesView.as_view(), name="youtube_episodes"),
    path("youtube_channels", YoutubeGalleryView.as_view(), name="youtube_gallery"),
    path(
        "podcasts/channels/<int:channel_id>",
        ChannelInfoView.as_view(),
        name="youtube_channel_info",
    ),
    path("podcasts", PodcastGalleryView.as_view(), name="podcast_gallery"),
    path("about", AboutView.as_view(), name="about"),
    path("podcast/<int:podcast_id>", PodcastInfoView.as_view(), name="podcast_info"),
    path("search_results", PodcastSearchResultsView.as_view(), name="search_results"),
    path(
        "youtube_search_results",
        YoutubeSearchResultsView.as_view(),
        name="youtube_search_results",
    ),
]
