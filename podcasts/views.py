from lib2to3.fixes.fix_input import context

from django.utils import timezone

from symtable import Class

import dateutil.parser
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Episode, Podcast, Channel, YoutubeEpisode
from podcasts.utils.helpers import get_twitter_tag

from django.db.models import Q
from django.views.generic.base import TemplateView


# HOME and ABOUT views
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


# About view - basic template
class AboutView(TemplateView):
    template_name = "podcasts/about.html"


# Home Page is list of Podcast episodes
class HomePageView(ListView):
    model = Episode
    paginate_by = 40
    ordering = "-pub_date"
    template_name = "podcasts/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        episodes = (
            Episode.objects.filter()
            .select_related("podcast_name")
            .order_by("-pub_date")
        )

        context["episodes"] = get_episode_list(episodes)
        return context


# list of all youtube episodes for a particular channel


class ChannelEpisodeListView(ListView):
    model = Channel
    paginate_by = 40
    template_name = "podcasts/channels/channel_info.html"

    # ordering = '-pub_date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        episodes = (
            YoutubeEpisode.objects.filter()
            .select_related("channel_name")
            .order_by("-pub_date")
        )

        context["yt_episodes"] = get_youtube_episode_list(episodes)
        return context


# List of all episodes for a particular podcast


class PodcastEpisodeListView(DetailView):
    model = Podcast
    template_name = "podcasts/podcast_info.html"
    paginate_by = 40
    ordering = "-pub_date"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        podcast = self.object

        context["episodes"] = get_episode_list(podcast.episode_set.all())
        return context


# list of all podcasts
class PodcastListView(ListView):
    model = Podcast
    template_name = "podcasts/podcast_gallery.html"

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


### List of all youtube channels
class YouTubeChannelView(ListView):
    model = Channel
    template_name = "podcasts/channels/channel_gallery.html"

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


# podcast search
class PodcastSearchResultsView(ListView):
    model = Episode
    template_name = "podcasts/search_results.html"
    context_object_name = "episodes"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if query:
            return Episode.objects.filter(
                Q(description__icontains=query) | Q(title__icontains=query)
            ).select_related("podcast_name")
        return Episode.objects.none()  # Return an empty queryset if no query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = get_episode_list(context["object_list"])
        context["query"] = self.request.GET.get("q", "")
        return context


# youtube search
class YouTubeSearchResultsView(ListView):
    model = YoutubeEpisode
    template_name = "podcasts/channels/search_results.html"
    context_object_name = "yt_episodes"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if query:
            return YoutubeEpisode.objects.filter(
                Q(description__icontains=query) | Q(title__icontains=query)
            ).select_related("channel_name")
        return YoutubeEpisode.objects.none()  # Return an empty queryset if no query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["yt_episodes"] = get_youtube_episode_list(context["object_list"])
        context["query"] = self.request.GET.get("q", "")
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
