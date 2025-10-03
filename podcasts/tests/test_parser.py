from datetime import datetime, timezone

from podcasts.parser.episode_parser import (
    populate_missing_fields,
    save_new_episodes,
    fetch_new_episodes,
)
from podcasts.parser.parse_utils import (
    convert_duration,
    episode_rss_lookup,
    passes_filter,
)
from unittest.mock import patch
from podcasts.models import Episode, Podcast
from podcasts.tests.mock_parser import mock_feed, mock_wot_feed
import pytest
from faker import Faker
import feedparser

from .factories import PodcastFactory, EpisodeFactory

fake = Faker()


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
        podcast = Podcast.objects.get_or_create(
            feed_href=mock_feed.href, podcast_name=mock_feed.channel.title
        )

        save_new_episodes(mock_feed)
        episode = Episode.objects.last()
        assert episode.description == "some description"
        assert episode.pub_date == datetime(2023, 4, 5, 1, 30, tzinfo=timezone.utc)
        assert str(episode.podcast_name) == "Test & Code"
        assert episode.guid == "a guid"


@pytest.mark.django_db
def test_save_new_episodes_with_filter():
    with patch("podcasts.parser.episode_parser.feedparser.parse") as mock_parse:
        mock_parse.return_value = mock_wot_feed
        podcast = Podcast.objects.get_or_create(
            feed_href=mock_feed.href,
            podcast_name=mock_feed.channel.title,
            requires_filter=True,
        )

        save_new_episodes(mock_wot_feed)
        episode = Episode.objects.last()
        assert episode.description == "wheel of description"


@pytest.mark.django_db
def test_fetch_new_episodes():
    PodcastFactory.create(
        feed_href="https://anchor.fm/s/1e036b78/podcast/rss",
    )
    with patch("podcasts.parser.episode_parser.populate_missing_fields"):
        with patch(
            "podcasts.parser.episode_parser.feedparser.parse"
        ) as mock_feedparser:
            mock_feedparser.return_value = mock_feed
            fetch_new_episodes()
            assert Episode.objects.last().title == "some title"


def test_convert_duration():
    # TODO parameterise
    assert convert_duration("5531") == "1:32:11"
    assert convert_duration("01:08:43") == "01:08:43"


@pytest.mark.django_db
def test_episode_rss_lookup():
    EpisodeFactory.create(guid="a guid")
    with patch("podcasts.parser.episode_parser.feedparser.parse") as mock_feedparser:
        mock_feedparser.return_value = mock_feed
        rss = episode_rss_lookup(Episode.objects.last())
        assert rss.title == "some title"
        assert rss.description == "some description"


@pytest.mark.django_db
def test_episode_rss_lookup_none():
    EpisodeFactory.create(guid="bleh")
    with patch("podcasts.parser.episode_parser.feedparser.parse") as mock_feedparser:
        mock_feedparser.return_value = mock_feed
        rss = episode_rss_lookup(Episode.objects.last())
        assert rss is None


@pytest.mark.django_db
def test_passes_filter():
    EpisodeFactory.create(title="Definitely wheel of time")
    with patch("podcasts.parser.episode_parser.feedparser.parse") as mock_feedparser:
        mock_feedparser.return_value = mock_wot_feed
        episode = Episode.objects.last()
        f = feedparser.parse(episode.link)
        item = f.entries[0]
        assert passes_filter(item) == True


@pytest.mark.django_db
def test_not_passes_filter():
    EpisodeFactory.create(title="Definitely wheel of time")
    with patch("podcasts.parser.episode_parser.feedparser.parse") as mock_feedparser:
        mock_feedparser.return_value = mock_feed
        episode = Episode.objects.last()
        f = feedparser.parse(episode.link)
        item = f.entries[0]
        assert passes_filter(item) == False
