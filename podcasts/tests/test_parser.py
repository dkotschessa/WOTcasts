import factory
from datetime import datetime, timezone

from podcasts.parser.episode_parser import (
    populate_missing_fields,
    save_new_episodes,
    fetch_new_episodes,
)
from podcasts.parser.parse_utils import convert_duration
from unittest.mock import patch
from podcasts.models import Episode, Podcast
from podcasts.tests.mock_parser import mock_feed
import pytest
from faker import Faker

fake = Faker()


class PodcastFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Podcast

    feed_href = "http://podcast1.com"


class EpisodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Episode

    title = "Another amazing episode"
    guid = fake.url()
    podcast_name = factory.SubFactory(PodcastFactory, feed_href="http://podcast.com")


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
def test_fetch_new_episodes():
    # Arrange
    PodcastFactory.create(feed_href="http://podcast1.com")
    PodcastFactory.create(feed_href="http://podcast2.com")

    with patch(
        "podcasts.parser.episode_parser.populate_missing_fields"
    ) as populate_mock:
        with patch(
            "podcasts.parser.episode_parser.save_new_episodes"
        ) as save_episodes_mock:
            fetch_new_episodes()

            populate_mock.assert_called()
            save_episodes_mock.assert_called()


def test_convert_duration():
    # TODO parameterise
    assert convert_duration("5531") == "1:32:11"
    assert convert_duration("01:08:43") == "01:08:43"
