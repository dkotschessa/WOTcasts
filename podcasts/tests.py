from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
from .models import Episode
from datetime import datetime

class PodcastTests(TestCase):
    def setUp(self):
        self.episode = Episode.objects.create(
            title = "My Awesome Podcast Episode",
            description = "hahah look",
            pub_date = timezone.now(),
            link = "http://hahaha.com",
            image = "https://image.something.com",
            podcast_name = "My Python Podcast",
            guid = "de194720-7b4c-49e2-a05f-432436d3fetr")
        
    

    def test_episode_content(self):
        self.assertEqual(self.episode.description, "hahah look")
        self.assertEqual(self.episode.link, "http://hahaha.com")
        self.assertEqual(self.episode.guid, "de194720-7b4c-49e2-a05f-432436d3fetr")

    def test_episode_str_representation(self):
        self.assertEqual(
            str(self.episode), "My Python Podcast: My Awesome Podcast Episode")
        
    def test_episode_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_tempalte(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "homepage.html")

    def test_homepage_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "My Awesome Podcast")

    
