from django.shortcuts import render
from django.views.generic import ListView
from .models import Episode, Podcast

from django.db.models import Q


def homepage_view(request):
    episodes = Episode.objects.filter().order_by("-pub_date")[:20]
    # TODO one of each
    context = {}

    episode_list = get_episode_list(episodes)
    context["episodes"] = episode_list
    return render(request, "podcasts/homepage.html", context)


def podcast_info_view(request, podcast_id):
    podcast = Podcast.objects.get(pk=podcast_id)
    episodes = Episode.objects.filter(podcast_name_id=podcast.id).order_by("-pub_date")[
        :20
    ]
    context = {"podcast": podcast}

    episode_list = get_episode_list(episodes)
    context["episodes"] = episode_list
    return render(request, "podcasts/podcast_info.html", context)


def search_results_view(request):
    query = request.GET.get("q")

    episodes = Episode.objects.filter(
        Q(description__icontains=query) | Q(title__icontains=query)
    )
    context = {}

    episode_list = get_episode_list(episodes)
    context["episodes"] = episode_list
    return render(request, "podcasts/homepage.html", context)


class SearchResultsView(ListView):
    model = Episode
    template_name = "podcasts/search_results.html"

    def get_queryset(self):
        object_list = Episode.objects.filter(
            Q(description__icontains=query) | Q(title__icontains=query)
        )
        return object_list


def get_episode_list(episodes):
    episode_list = []
    for episode in episodes:
        context_dict = {
            "episode_image": episode.image,
            "podcast_name": episode.podcast_name,
            "podcast_title": episode.title,
            "episode_description": episode.description,
            "episode_duration": episode.duration,
            "episode_link": episode.link,
            "podcast_id": episode.podcast_name_id,
            "published_date": episode.pub_date,
        }
        episode_list.append(context_dict)
    return episode_list


def podcast_gallery_view(request):
    podcasts = Podcast.objects.all()
    podcast_list = []
    context = {}
    for podcast in podcasts:
        context_dict = {
            "podcast_name": podcast.podcast_name,
            "podcast_summary": podcast.podcast_summary,
            "podcast_image": podcast.podcast_image,
            "podcast_id": podcast.id,
        }
        podcast_list.append(context_dict)

    context["podcasts"] = podcast_list
    return render(request, "podcasts/podcast_gallery.html", context)
