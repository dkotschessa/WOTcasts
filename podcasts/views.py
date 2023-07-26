from django.shortcuts import render
from django.views.generic import ListView
from .models import Episode, Podcast


def homepage_view(request):
    episodes = Episode.objects.filter().order_by("-pub_date")[:20]
    #TODO one of each
    podcast_id = episodes[0].podcast_name_id
    episode_list = []
    context = {}
    for episode in episodes:
        context_dict = {}
        context_dict["episode_image"] = episode.image
        context_dict["podcast_name"] = episode.podcast_name
        context_dict["podcast_title"] = episode.title
        context_dict["episode_description"] = episode.description
        context_dict["episode_link"] = episode.link
        context_dict["podcast_id"] = podcast_id
        episode_list.append(context_dict)
    context["episodes"] = episode_list
    return render(request, "podcasts/homepage.html", context)


def podcast_info_view(request, podcast_id):
    podcast = Podcast.objects.get(pk=podcast_id)

    return render(
        request, "podcasts/podcast_info.html", {"podcast" : podcast}
    )

