from django.shortcuts import render
from django.views.generic import ListView
from .models import Episode, Podcast

class HomePageView(ListView):
    template_name = "homepage.html"
    model = Episode


     
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episodes = Episode.objects.filter().order_by("-pub_date")[:50]
        podcast_id = episodes[0].podcast_name_id
        episode_list = []
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
        return context





def podcast_info_view(request, podcast_id):
    podcast = Podcast.objects.get(pk=podcast_id)

    return render(
        request, "podcast_info.html", {"podcast" : podcast}
    )
        #
        #
        # context = {}
        # context['podcast_href'] = podcast.feed_href
        # context['podcast_name'] = podcast.podcast_name
        # context['podcast_summary'] = podcast.podcast_summary
        # context['podcast_image'] = podcast.podcast_image
        # return context


