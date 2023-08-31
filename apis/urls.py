from django.urls import path
from .views import PodcastAPIview

urlpatterns = [path("", PodcastAPIview.as_view(), name="podcast_list")]
