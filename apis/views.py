from rest_framework import generics
from podcasts.models import Podcast
from .serializers import PodcastSerializer


# Create your views here.
class PodcastAPIview(generics.ListAPIView):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
