from django.shortcuts import render
from django.views.generic import ListView
from .models import Episode, Podcast


def homepage_view(request):
    episodes = Episode.objects.filter().order_by("-pub_date")[:20]
    #TODO one of each
    episode_list = []
    context = {}
    for episode in episodes:
        context_dict = {}
        context_dict["episode_image"] = episode.image
        context_dict["podcast_name"] = episode.podcast_name
        context_dict["podcast_title"] = episode.title
        context_dict["episode_description"] = episode.description
        context_dict["episode_link"] = episode.link
        context_dict["podcast_id"] = episode.podcast_name_id
        episode_list.append(context_dict)
    context["episodes"] = episode_list
    return render(request, "podcasts/homepage.html", context)

def podcast_info_view(request, podcast_id):
    podcast = Podcast.objects.get(pk=podcast_id)
    episodes = Episode.objects.filter(podcast_name_id=podcast.id).order_by("-pub_date")[:20]
    episode_list = []
    context = {"podcast" : podcast}
    for episode in episodes:
        context_dict = {}
        context_dict["episode_image"] = episode.image
        context_dict["podcast_name"] = episode.podcast_name
        context_dict["podcast_title"] = episode.title
        context_dict["episode_description"] = episode.description
        context_dict["episode_link"] = episode.link
        context_dict["podcast_id"] = episode.podcast_name_id
        episode_list.append(context_dict)
    context["episodes"] = episode_list
    return render(
        request, "podcasts/podcast_info.html", context
    )



def podcast_gallery_view(request):
    podcasts = Podcast.objects.all()
    podcast_list = []
    context = {}
    for podcast in podcasts:
        context_dict = {}
        context_dict['podcast_name'] = podcast.podcast_name
        context_dict['podcast_summary'] = podcast.podcast_summary
        context_dict['podcast_image'] = podcast.podcast_image
        context_dict["podcast_id"] = podcast.id
        podcast_list.append(context_dict)

    context['podcasts'] = podcast_list
    return render(request, "podcasts/podcast_gallery.html", context)





