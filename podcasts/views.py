import datetime

import dateutil.parser
from django.shortcuts import render, redirect
from .models import Episode, Podcast, Channel, YoutubeEpisode
from podcasts.utils.helpers import get_twitter_tag

from django.db.models import Q


# HOME and ABOUT views


def homepage_view(request):
    episodes = (
        Episode.objects.filter()
        .prefetch_related("podcast_name")
        .order_by("-pub_date")[:40]
    )
    # TODO one of each
    context = {}

    episode_list = get_episode_list(episodes)
    context["episodes"] = episode_list
    return render(request, "podcasts/homepage.html", context)


def about_view(request):
    return render(request, "podcasts/about.html")


# PODCAST views


def podcast_info_view(request, podcast_id):
    podcast = Podcast.objects.get(pk=podcast_id)
    episodes = Episode.objects.filter(podcast_name_id=podcast.id).order_by("-pub_date")[
        :40
    ]
    context = {"podcast": podcast}

    episode_list = get_episode_list(episodes)
    context["episodes"] = episode_list
    return render(request, "podcasts/podcast_info.html", context)


def podcast_gallery_view(request):
    podcasts = Podcast.objects.all()
    podcast_list = []
    context = {}
    for podcast in podcasts:
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
    return render(request, "podcasts/podcast_gallery.html", context)


# Podcast search


def podcast_search_results_view(request):
    query = request.GET.get("q")

    episodes = Episode.objects.filter(
        Q(description__icontains=query) | Q(title__icontains=query)
    )
    context = {}

    episode_list = get_episode_list(episodes)
    context["episodes"] = episode_list
    context["query"] = query
    return render(request, "podcasts/search_results.html", context)


def youtube_search_results_view(request):
    query = request.GET.get("q")

    episodes = YoutubeEpisode.objects.filter(
        Q(description__icontains=query) | Q(title__icontains=query)
    )
    context = {}

    episode_list = get_youtube_episode_list(episodes)
    context["yt_episodes"] = episode_list
    context["query"] = query
    return render(request, "podcasts/channels/search_results.html", context)


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


### YOUTUBE views


def youtube_gallery_view(request):
    channels = Channel.objects.all()
    channel_list = []
    context = {}
    for channel in channels:
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
    return render(request, "podcasts/channels/channel_gallery.html", context)


def youtube_episodes_view(request):
    yt_episodes = (
        YoutubeEpisode.objects.filter()
        .prefetch_related("channel_name")
        .order_by("-pub_date")[:40]
    )

    context = {}

    episode_list = get_youtube_episode_list(yt_episodes)
    context["yt_episodes"] = episode_list
    return render(request, "podcasts/channels/youtube.html", context)


def channel_info_view(request, channel_id):
    channel = Channel.objects.get(pk=channel_id)
    episodes = YoutubeEpisode.objects.filter(channel_name=channel_id).order_by(
        "-pub_date"
    )[:40]
    context = {"channel": channel}

    episode_list = get_youtube_episode_list(episodes)
    context["yt_episodes"] = episode_list
    return render(request, "podcasts/channels/channel_info.html", context)


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


def get_content_by_date_view(request, content_date: str):
    date = dateutil.parser.parse(content_date)
    podcast_episodes = Episode.objects.filter(pub_date__date=date)
    yt_episodes = YoutubeEpisode.objects.filter(pub_date__date=date)
    podcast_episode_list = get_episode_list(podcast_episodes)
    youtube_episode_list = get_youtube_episode_list(yt_episodes)
    context = {
        "pub_date": content_date,
        "podcast_episodes": podcast_episode_list,
        "youtube_episodes": youtube_episode_list,
    }
    return render(request, "podcasts/content_by_date.html", context)


def get_content_by_date_range_view(request, start_date: str, end_date: str):
    content_start_date = dateutil.parser.parse(start_date)
    content_end_date = dateutil.parser.parse(end_date)
    podcast_episodes = Episode.objects.filter(
        pub_date__date__gte=content_start_date
    ).filter(pub_date__date__lte=content_end_date)
    yt_episodes = YoutubeEpisode.objects.filter(
        pub_date__date__gte=content_start_date
    ).filter(pub_date__date__lte=content_end_date)
    podcast_episode_list = get_episode_list(podcast_episodes)
    youtube_episode_list = get_youtube_episode_list(yt_episodes)
    context = {
        "start_date": content_start_date.date,
        "end_date": content_end_date.date,
        "podcast_episodes": podcast_episode_list,
        "youtube_episodes": youtube_episode_list,
    }
    return render(request, "podcasts/content_by_date.html", context)
