from django.shortcuts import render
from django.views.generic import ListView
from .models import Episode

class HomePageView(ListView):
    template_name = "homepage.html"
    model = Episode


     
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episodes = Episode.objects.filter().order_by("-pub_date")[:50]
        episode_list = []
        for episode in episodes:
            context_dict = {}
            context_dict["episode_image"] = episode.image
            context_dict["podcast_name"] = episode.podcast_name
            context_dict["podcast_title"] = episode.title
            context_dict["episode_description"] = episode.description
            context_dict["episode_link"] = episode.link
            episode_list.append(context_dict)
        context["episodes"] = episode_list
        return context