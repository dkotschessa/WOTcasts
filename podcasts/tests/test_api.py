from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from podcasts.models import Podcast


class APITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.podcast = Podcast.objects.create(
            feed_href="www.something.com",
            podcast_name="A test podcast",
            requires_filter=False,
        )

    def test_api_listview(self):
        response = self.client.get(reverse("podcast_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response.self.book)
