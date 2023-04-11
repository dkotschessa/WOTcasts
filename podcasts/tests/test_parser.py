from typing import List
from django.test import TestCase
import feedparser
from datetime import datetime, timezone
from podcasts.parser.episode_parser import populate_missing_fields, save_new_episodes, get_rss_feed_list, fetch_new_episodes
from unittest.mock import patch, Mock
from podcasts.models import Episode, Podcast
from podcasts.tests.mock_parser import mock_feed
import pytest



@pytest.mark.django_db
def test_populate_missing_fields():
    Podcast.objects.create(feed_href="https://feeds.fireside.fm/testandcode/rss")
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

@pytest.mark.django_db
def test_save_new_episodes():
        with patch("podcasts.parser.episode_parser.feedparser.parse") as mock_parse:

            mock_parse.return_value = mock_feed
            podcast = Podcast.objects.get_or_create(feed_href = mock_feed.href, podcast_name = mock_feed.channel.title)

            save_new_episodes(mock_feed)
            episode = Episode.objects.last()
            assert episode.description == "some description"
            assert episode.pub_date == datetime(2023, 4, 5, 1, 30, tzinfo=timezone.utc)
            assert str(episode.podcast_name)  == "Test & Code"
            assert episode.guid == "a guid"


@pytest.mark.django_db
def test_get_rss_feed_list():
    podcast_1 = Podcast(feed_href = "http://podcast1.com")
    podcast_1.save()
    podcast_2 = Podcast(feed_href = "http://podcast2.com")
    podcast_2.save()
    list = get_rss_feed_list()
    assert len(list) == 2


@pytest.mark.django_db
def test_fetch_new_episodes():
     with patch("podcasts.parser.episode_parser.populate_missing_fields") as populate:
          with patch("podcasts.parser.episode_parser.get_rss_feed_list") as feed_list_mock:
               feed_list_mock.return_value = ["http://podcast1.com","http://podcast2.com" ]
               with patch("podcasts.parser.episode_parser.save_new_episodes") as save_new_episodes_mock:
                with patch("podcasts.parser.episode_parser.feedparser.parse") as feedparser_mock:
                    fetch_new_episodes()
                    populate.assert_called()
                    feed_list_mock.assert_called()
                    assert save_new_episodes_mock.call_count == 2
                    assert feedparser_mock.call_count == 2
                    feedparser_mock.assert_called_with('http://podcast2.com')


