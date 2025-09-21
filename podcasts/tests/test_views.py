from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
from podcasts.models import Episode, Podcast
from unittest import skipIf
import django
from podcasts.views import get_episode_list

DJANGO_VERSION = float(django.get_version()[:2])


class PodcastTests(TestCase):
    def setUp(self):
        self.podcast = Podcast.objects.create(
            podcast_name="My Python Podcast",
            feed_href="http://something.rss/",
            podcast_summary="this is a summary",
            podcast_image="this is a link to an image",
            id=1,
        )
        self.podcast.save()
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
        self.episode.save()

    def test_episode_content(self):
        self.assertEqual(self.episode.description, "hahah look")
        self.assertEqual(self.episode.link, "http://hahaha.com")
        self.assertEqual(self.episode.guid, "de194720-7b4c-49e2-a05f-432436d3fetr")

    def test_episode_str_representation(self):
        self.assertEqual(
            str(self.episode), "My Python Podcast: My Awesome Podcast Episode"
        )

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "podcasts/homepage.html")

    def test_home_page_n_plus_one(self):
        with self.assertNumQueries(2):
            self.client.get(reverse("homepage"))

    def test_homepage_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "My Python Podcast")

    def test_get_episode_list(self):
        episodes = get_episode_list(Episode.objects.all())
        self.assertEquals(episodes[0]["episode_image"], "https://image.something.com")
        self.assertEquals(episodes[0]["episode_title"], "My Awesome Podcast Episode")
        ## todo episode name is not right. it is returning and object

    def test_episode_list_n_plus_one(self):
        with self.assertNumQueries(2):
            get_episode_list(Episode.objects.all())

    def test_podcast_gallery_n_plus_one(self):
        with self.assertNumQueries(1):
            self.client.get(reverse("podcast_gallery"))

    def test_podcast_info_view(self):
        page = reverse("podcast_info", args=[1])
        response = self.client.get(page)
        self.assertEqual(response.status_code, 200)

    def test_podcast_info_view_n_plus_one(self):
        with self.assertNumQueries(2):
            self.client.get(reverse("podcast_info", args=[1]))

    def test_get_pk_that_aint_there(self):
        response = self.client.get(reverse("podcast_info", args=[234324]))
        self.assertEqual(response.status_code, 404)

    @skipIf(DJANGO_VERSION < 5.0, "Django >= 5.0")
    def test_podcast_search_query(self):
        page = reverse("search_results", query={"q": "look"})
        response = self.client.get(page)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")

    @skipIf(DJANGO_VERSION < 5.0, "Django >= 5.0")
    def test_podcast_search_none(self):
        search_term = "?q=wheel"
        page = reverse("search_results", query={})
        response = self.client.get(page)
        self.assertEqual(response.status_code, 200)
