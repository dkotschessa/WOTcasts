from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
from podcasts.models import Episode, Podcast
from rest_framework import status

from podcasts.views import get_episode_list


class PodcastTests(TestCase):
    def setUp(self):
        self.podcast = Podcast.objects.create(
            podcast_name="My Python Podcast",
            feed_href="http://something.rss/",
            podcast_summary="this is a summary",
            podcast_image="this is a link to an image",
        )
        self.episode = Episode.objects.create(
            title="My Awesome Podcast Episode",
            description="hahah look",
            pub_date=timezone.now(),
            link="http://hahaha.com",
            image="https://image.something.com",
            podcast_name=self.podcast,
            guid="de194720-7b4c-49e2-a05f-432436d3fetr",
            announced_to_twitter=True,
        )

    def test_episode_content(self):
        self.assertEqual(self.episode.description, "hahah look")
        self.assertEqual(self.episode.link, "http://hahaha.com")
        self.assertEqual(self.episode.guid, "de194720-7b4c-49e2-a05f-432436d3fetr")

    def test_episode_str_representation(self):
        self.assertEqual(
            str(self.episode), "My Python Podcast: My Awesome Podcast Episode"
        )

    def test_episode_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "podcasts/homepage.html")

    def test_home_page_n_plus_one(self):
        with self.assertNumQueries(1):
            self.client.get(reverse("homepage"))

    def test_homepage_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "My Python Podcast")

    def test_get_episode_list(self):
        episode = get_episode_list(Episode.objects.filter(id=1))[0]
        self.assertEquals(episode["episode_image"], "https://image.something.com")
        self.assertEquals(episode["episode_title"], "My Awesome Podcast Episode")
        ## todo episode name is not right. it is returning and object

    def test_num_queries_not_n_plus_one(self):
        with self.assertNumQueries(1):
            get_episode_list(Episode.objects.filter(id=1))[0]
