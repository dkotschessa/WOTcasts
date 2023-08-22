from bs4 import BeautifulSoup

from podcasts.parser.youtube_parser import (
    soup_tube,
    get_rss_link_from_channel,
    get_description,
    channel_dict,
    populate_missing_youtube_fields,
    save_new_youtube_episodes,
    fetch_new_youtube_episodes,
    get_xml,
)
from podcasts.models import Channel, YoutubeEpisode
from unittest.mock import patch
import factory
import pytest
from .samplehtml import sample_html, sample_xml

test_urls = ["https://www.youtube.com/@WoTUp", "https://www.youtube.com/@TheDustyWheel"]

from faker import Faker

fake = Faker()


class ChannelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Channel

    youtube_url = fake.url()


class YoutubeEpisodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = YoutubeEpisode

    title = "Another amazing video"
    pub_date = fake.date()
    link = fake.url()
    image = fake.url()
    guid = fake.url()
    channel_name = factory.SubFactory(ChannelFactory, youtube_url=fake.url())
    duration = "1022"


def test_soup_tube():
    with patch("podcasts.parser.youtube_parser.requests.get") as mock_requests:
        mock_requests.return_value = sample_html
        soup = soup_tube("http://amazingwebsite.com")
        assert len(soup.find_all("a")) == 3


def test_get_rss_from_channel():
    with patch("podcasts.parser.youtube_parser.soup_tube") as mock_soup_tube:
        soup = BeautifulSoup(sample_html.content, "html.parser")
        mock_soup_tube.return_value = soup
        feed = get_rss_link_from_channel("http://amazingwebsite.com")
        assert feed == "https://www.youtube.com/feeds/videos.xml?channel_id=ABCDEFG"


def test_get_xml():
    # Arrange
    url = "http://www.someradxml.com"
    with patch(
        "podcasts.parser.youtube_parser.get_rss_link_from_channel"
    ) as mock_get_rss:
        mock_get_rss.return_value = sample_xml.content
        # ACT
        feed = get_xml(url)
        # ASSERT
        assert mock_get_rss.call_args(url)
        assert feed.channel.title == "WoT Up!"


def test_get_description():
    # ARRANGE
    with patch("podcasts.parser.youtube_parser.requests.get") as mock_requests:
        mock_requests.return_value = sample_html
        # ACT
        description = get_description("http://amazingwebsite.com")
        # ASSERT
        assert description == "This is a description it is very exciting"


def test_channel_dict():
    # Arrange
    url = "http://www.someradxml.com"
    with patch(
        "podcasts.parser.youtube_parser.get_rss_link_from_channel"
    ) as mock_get_rss:
        mock_get_rss.return_value = sample_xml.content

        with patch(
            "podcasts.parser.youtube_parser.get_description"
        ) as mock_description:
            mock_description.return_value = "Here's a description"
            # ACT
            fields = channel_dict(url)
            # ASSERT
            assert list(fields.keys()) == [
                "feed_href",
                "channel_name",
                "description",
                "image",
                "host",
            ]


@pytest.mark.django_db
def test_populate_missing_youtube_fields():
    # ARRANGE
    new_channel = ChannelFactory.create()
    channel_fields = {
        "feed_href": "http://www.youtube.com/feeds/videos.xml?channel_id=UCbl0nJfwdXWANnKEURnFkHg",
        "channel_name": "WoT Up!",
        "description": "Here's a description",
        "image": "https://i2.ytimg.com/vi/IIURJk6ynwk/hqdefault.jpg",
        "host": "WoT Up!",
    }
    with patch("podcasts.parser.youtube_parser.channel_dict") as mock_channel_dict:
        mock_channel_dict.return_value = channel_fields
        populate_missing_youtube_fields()
        new_fields = Channel.objects.get(youtube_url=new_channel.youtube_url)

        assert new_fields.channel_name == channel_fields["channel_name"]
        assert new_fields.feed_href == channel_fields["feed_href"]
        assert new_fields.channel_summary == channel_fields["description"]
        assert new_fields.channel_image == channel_fields["image"]
        assert new_fields.host == channel_fields["host"]

        # TODO create a blank url'ed channel


@pytest.mark.django_db
def test_save_new_youtube_episodes():
    with patch("podcasts.parser.youtube_parser.get_xml") as mock_get_xml:
        pass


@pytest.mark.django_db
def test_fetch_new_youtube_episodes():
    # ARRANGE

    test_url = fake.url()
    episode = YoutubeEpisodeFactory.create(link=test_url)
    url = episode.link

    with patch(
        "podcasts.parser.youtube_parser.populate_missing_youtube_fields"
    ) as mock_populate, patch(
        "podcasts.parser.youtube_parser.save_new_youtube_episodes"
    ) as save_new_youtube_episodes_mock:
        # ACT
        fetch_new_youtube_episodes()

        mock_populate.assert_called()
        save_new_youtube_episodes_mock.assert_called()

    # ASSERT
    assert url == test_url
