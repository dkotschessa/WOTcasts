from django.urls import path

from .views import (
    PodcastListView,
    AboutView,
    HomePageView,
    YouTubeSearchResultsView,
    PodcastEpisodeListView,
    PodcastSearchResultsView,
    ChannelEpisodeListView,
    YouTubeChannelView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("wheel_of_youtube", ChannelEpisodeListView.as_view(), name="youtube_episodes"),
    path("youtube_channels", YouTubeChannelView.as_view(), name="youtube_gallery"),
    path(
        "podcasts/channels/<int:channel_id>",
        ChannelEpisodeListView.as_view(),
        name="youtube_channel_info",
    ),
    path("podcasts", PodcastListView.as_view(), name="podcast_gallery"),
    path("about", AboutView.as_view(), name="about"),
    path("podcast/<int:pk>", PodcastEpisodeListView.as_view(), name="podcast_info"),
    path("search_results", PodcastSearchResultsView.as_view(), name="search_results"),
    path(
        "youtube_search_results",
        YouTubeSearchResultsView.as_view(),
        name="youtube_search_results",
    ),
]
