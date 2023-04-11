from typing import List
from django.test import TestCase
import feedparser
from podcasts.parser.episode_parser import populate_missing_fields, save_new_episodes
from unittest.mock import patch
from podcasts.models import Episode, Podcast
from podcasts.tests.mock_parser import mock_feed


class PodcastTests(TestCase):
    def setUp(self):  # TODO factory
        Podcast.objects.create(feed_href="https://feeds.fireside.fm/testandcode/rss")

    def test_populate_missing_fields(self):
        with patch("podcasts.parser.episode_parser.feedparser.parse") as mock_parse:
            mock_parse.return_value = mock_feed
            populate_missing_fields()  
            podcast = Podcast.objects.last()
            assert podcast.podcast_name == "Test & Code"
            assert (
                "Topics include automated testing, testing strategy"
                in podcast.podcast_summary
            )
            assert (
                podcast.podcast_image
                == "https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover.jpg"
            )
    def test_save_new_episodes(self):
        feed = feedparser.parse("https://feeds.fireside.fm/testandcode/rss")
        save_new_episodes(feed)
        episode = Episode.objects.last()
        assert episode.description == ""
        assert episode.pub_date == ""
        assert episode.podcast_name  == ""
        assert episode.guid == ""
