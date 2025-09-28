import datetime

import dateutil.parser
from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Episode, Podcast, Channel, YoutubeEpisode
from podcasts.utils.helpers import get_twitter_tag

from django.db.models import Q


# HOME and ABOUT views


class EpisodeListMixin:
    """Mixin to transform an Episode queryset into the required dictionary format."""

    context_object_name = "episodes"

    def get_episode_list_data(self, queryset):
        episode_list = []
        for episode in queryset:
            episode_list.append(
                {
                    "episode_image": episode.image,
                    "podcast_name": episode.podcast_name,
                    "episode_title": episode.title,
                    "episode_description": episode.description,
                    "episode_duration": episode.duration,
                    "episode_link": episode.link,
                    "podcast_id": episode.podcast_name_id,
                    "published_date": episode.pub_date,
                }
            )
        return episode_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Transform the object_list (queryset result) before passing to template
        context[self.context_object_name] = self.get_episode_list_data(
            context["object_list"]
        )
        return context


class SearchQueryMixin:
    """Mixin to handle the common 'q' query parameter for search views."""

    def get_queryset(self):
        # Store the query for use in get_context_data
        self.query = self.request.GET.get("q", "")
        if self.query:
            # The actual filtering logic must be implemented by the inheriting class
            # because the model changes (Episode or YoutubeEpisode).
            return (
                super()
                .get_queryset()
                .filter(
                    Q(description__icontains=self.query)
                    | Q(title__icontains=self.query)
                )
            )
        return self.model.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.query
        return context


class HomepageView(EpisodeListMixin, ListView):
    """
    Replaces homepage_view
    """

    model = Episode
    template_name = "podcasts/homepage.html"
    context_object_name = "episodes"  # By default it's object_list

    def get_queryset(self):
        # Fetch the episodes, similar to the original function
        return (
            Episode.objects.all()
            .select_related("podcast_name")
            .order_by("-pub_date")[:40]
        )

    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Apply the transformation logic from get_episode_list
    #     context[self.context_object_name] = get_episode_list(context["object_list"])
    #     return context


class AboutView(TemplateView):
    template_name = "podcasts/about.html"


# PODCAST views


class PodcastInfoView(DetailView):
    model = Podcast
    pk_url_kwarg = "podcast_id"  # Expects 'podcast_id' from URLconf
    template_name = "podcasts/podcast_info.html"
    context_object_name = "podcast"  # By default it's object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        podcast = self.object  # The Podcast object fetched by DetailView
        episodes = (
            Episode.objects.filter(podcast_name_id=podcast.id)
            .select_related("podcast_name")
            .order_by("-pub_date")[:40]
        )
        context["episodes"] = get_episode_list(episodes)
        return context


class PodcastGalleryView(ListView):
    model = Podcast
    template_name = "podcasts/podcast_gallery.html"
    context_object_name = "podcasts"  # Will contain the formatted list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        podcast_list = []
        for podcast in context["object_list"]:
            context_dict = {
                "podcast_name": podcast.podcast_name,
                "podcast_summary": podcast.podcast_summary,
                "podcast_twitter_url": podcast.podcast_twitter,
                "podcast_twitter_tag": get_twitter_tag(podcast.podcast_twitter),
                "podcast_image": podcast.podcast_image,
                "podcast_id": podcast.id,
            }
            podcast_list.append(context_dict)

        context["podcasts"] = podcast_list
        return context


# Podcast search


class PodcastSearchResultsView(SearchQueryMixin, EpisodeListMixin, ListView):
    """
    Replaces podcast_search_results_view
    """

    model = Episode
    template_name = "podcasts/search_results.html"
    # context_object_name = "episodes"
    #
    # def get_queryset(self):
    #     # Get the 'q' query parameter from the URL
    #     self.query = self.request.GET.get("q", "")
    #     if self.query:
    #         return Episode.objects.filter(
    #             Q(description__icontains=self.query) | Q(title__icontains=self.query)
    #         )
    #     return Episode.objects.none()  # Return empty queryset if no query
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Apply the transformation logic from get_episode_list
    #     context[self.context_object_name] = get_episode_list(context["object_list"])
    #     context["query"] = self.query
    #     return context


def get_episode_list(episodes):
    episode_list = []
    for episode in episodes:
        context_dict = {
            "episode_image": episode.image,
            "podcast_name": episode.podcast_name,
            "episode_title": episode.title,
            "episode_description": episode.description,
            "episode_duration": episode.duration,
            "episode_link": episode.link,
            "podcast_id": episode.podcast_name_id,
            "published_date": episode.pub_date,
        }
        episode_list.append(context_dict)
    return episode_list


# PODCAST VIEWS


class EpisodeListMixin:
    """Mixin to transform an Episode queryset into the required dictionary format."""

    context_object_name = "episodes"

    def get_episode_list_data(self, queryset):
        episode_list = []
        for episode in queryset:
            episode_list.append(
                {
                    "episode_image": episode.image,
                    "podcast_name": episode.podcast_name,
                    "episode_title": episode.title,
                    "episode_description": episode.description,
                    "episode_duration": episode.duration,
                    "episode_link": episode.link,
                    "podcast_id": episode.podcast_name_id,
                    "published_date": episode.pub_date,
                }
            )
        return episode_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Transform the object_list (queryset result) before passing to template
        context[self.context_object_name] = self.get_episode_list_data(
            context["object_list"]
        )
        return context


class YoutubeEpisodeListMixin:
    """Mixin to transform a YoutubeEpisode queryset into the required dictionary format."""

    context_object_name = "yt_episodes"

    def get_youtube_episode_list_data(self, queryset):
        episode_list = []
        for episode in queryset:
            episode_list.append(
                {
                    "episode_image": episode.image,
                    "channel_name": episode.channel_name,
                    "episode_title": episode.title,
                    "episode_description": episode.description,
                    "episode_link": episode.link,
                    "channel_id": episode.channel_name_id,
                    "published_date": episode.pub_date,
                }
            )
        return episode_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_youtube_episode_list_data(
            context["object_list"]
        )
        return context


class YoutubeSearchResultsView(SearchQueryMixin, YoutubeEpisodeListMixin, ListView):
    model = YoutubeEpisode
    template_name = "podcasts/channels/search_results.html"
    # context_object_name = "yt_episodes"
    #
    # def get_queryset(self):
    #     self.query = self.request.GET.get("q", "")
    #     if self.query:
    #         return YoutubeEpisode.objects.filter(
    #             Q(description__icontains=self.query) | Q(title__icontains=self.query)
    #         )
    #     return YoutubeEpisode.objects.none()
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Apply the transformation logic from get_youtube_episode_list
    #     context[self.context_object_name] = get_youtube_episode_list(
    #         context["object_list"]
    #     )
    #     context["query"] = self.query
    #     return context


class EpisodeListMixin:
    """Mixin to transform an Episode queryset into the required dictionary format."""

    context_object_name = "episodes"

    def get_episode_list_data(self, queryset):
        episode_list = []
        for episode in queryset:
            episode_list.append(
                {
                    "episode_image": episode.image,
                    "podcast_name": episode.podcast_name,
                    "episode_title": episode.title,
                    "episode_description": episode.description,
                    "episode_duration": episode.duration,
                    "episode_link": episode.link,
                    "podcast_id": episode.podcast_name_id,
                    "published_date": episode.pub_date,
                }
            )
        return episode_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Transform the object_list (queryset result) before passing to template
        context[self.context_object_name] = self.get_episode_list_data(
            context["object_list"]
        )
        return context


class YoutubeEpisodeListMixin:
    """Mixin to transform a YoutubeEpisode queryset into the required dictionary format."""

    context_object_name = "yt_episodes"

    def get_youtube_episode_list_data(self, queryset):
        episode_list = []
        for episode in queryset:
            episode_list.append(
                {
                    "episode_image": episode.image,
                    "channel_name": episode.channel_name,
                    "episode_title": episode.title,
                    "episode_description": episode.description,
                    "episode_link": episode.link,
                    "channel_id": episode.channel_name_id,
                    "published_date": episode.pub_date,
                }
            )
        return episode_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.get_youtube_episode_list_data(
            context["object_list"]
        )
        return context


class YoutubeGalleryView(ListView):
    model = Channel
    template_name = "podcasts/channels/channel_gallery.html"
    context_object_name = "channels"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel_list = []
        for channel in context["object_list"]:
            context_dict = {
                "youtube_url": channel.youtube_url,
                "feed_href": channel.feed_href,
                "channel_name": channel.channel_name,
                "channel_summary": channel.channel_summary,
                "channel_image": channel.channel_image,
                "channel_twitter_url": channel.channel_twitter,
                "channel_twitter_tag": get_twitter_tag(channel.channel_twitter),
                "host": channel.host,
                "channel_id": channel.id,
            }
            channel_list.append(context_dict)

        context["channels"] = channel_list
        return context


class YoutubeEpisodesView(YoutubeEpisodeListMixin, ListView):
    model = YoutubeEpisode
    template_name = "podcasts/channels/youtube.html"
    context_object_name = "yt_episodes"

    def get_queryset(self):
        return (
            YoutubeEpisode.objects.all()
            .prefetch_related("channel_name")
            .order_by("-pub_date")[:40]
        )

    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Apply the transformation logic from get_youtube_episode_list
    #     context[self.context_object_name] = get_youtube_episode_list(
    #         context["object_list"]
    #     )
    #     return context


class ChannelInfoView(DetailView):
    model = Channel
    pk_url_kwarg = "channel_id"
    template_name = "podcasts/channels/channel_info.html"
    context_object_name = "channel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        channel = self.object
        episodes = YoutubeEpisode.objects.filter(channel_name=channel.id).order_by(
            "-pub_date"
        )[:40]
        context["yt_episodes"] = get_youtube_episode_list(episodes)
        return context


def get_youtube_episode_list(episodes):
    episode_list = []
    for episode in episodes:
        context_dict = {
            "episode_image": episode.image,
            "channel_name": episode.channel_name,
            "episode_title": episode.title,
            "episode_description": episode.description,
            "episode_link": episode.link,
            "channel_id": episode.channel_name_id,
            "published_date": episode.pub_date,
        }
        episode_list.append(context_dict)
    return episode_list


class ContentByDateView(TemplateView):
    template_name = "podcasts/content_by_date.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_date = self.kwargs["content_date"]  # Get from URL kwarg

        try:
            date = dateutil.parser.parse(content_date)
        except dateutil.parser.ParserError:
            # You might want to handle this error more gracefully
            raise Http404("Invalid date format.")

        podcast_episodes = Episode.objects.filter(pub_date__date=date)
        yt_episodes = YoutubeEpisode.objects.filter(pub_date__date=date)

        context.update(
            {
                "pub_date": content_date,
                "podcast_episodes": get_episode_list(podcast_episodes),
                "youtube_episodes": get_youtube_episode_list(yt_episodes),
            }
        )
        return context


class ContentByDateRangeView(TemplateView):
    template_name = "podcasts/content_by_date.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date_str = self.kwargs["start_date"]
        end_date_str = self.kwargs["end_date"]

        try:
            content_start_date = dateutil.parser.parse(start_date_str)
            content_end_date = dateutil.parser.parse(end_date_str)
        except dateutil.parser.ParserError:
            raise Http404("Invalid date format in range.")

        podcast_episodes = Episode.objects.filter(
            pub_date__date__gte=content_start_date.date(),
            pub_date__date__lte=content_end_date.date(),
        )
        yt_episodes = YoutubeEpisode.objects.filter(
            pub_date__date__gte=content_start_date.date(),
            pub_date__date__lte=content_end_date.date(),
        )

        context.update(
            {
                "start_date": content_start_date.date(),
                "end_date": content_end_date.date(),
                "podcast_episodes": get_episode_list(podcast_episodes),
                "youtube_episodes": get_youtube_episode_list(yt_episodes),
            }
        )
        return context
