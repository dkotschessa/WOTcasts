from typing import Dict
from feedparser.util import FeedParserDict
from dateutil import parser as date_parser
from podcasts.models import Channel, YoutubeEpisode
import requests
from bs4 import BeautifulSoup
import feedparser
import logging

logger = logging.getLogger(__name__)


def soup_tube(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_rss_link_from_channel(url):
    soup = soup_tube(url)
    feed_href = soup.find(title="RSS")
    return feed_href["href"]


def get_xml(url):
    feed_href = get_rss_link_from_channel(url)
    feed = feedparser.parse(feed_href)
    return feed


def get_description(url):
    """
    Gets description from the original youtube channel
    as XML doesn't have anything good

    """
    soup = soup_tube(url)
    og_description = soup.find("meta", property="og:description")
    description = og_description.get("content")
    return description


def get_thumbnail(url):
    """
    TODO
    get channel thumbnail from youtube channel
    it's deeply nested so this is a bit painful
    """
    pass


def channel_dict(url) -> Dict:
    feed = get_xml(url)

    return {
        "feed_href": feed.channel.links[0]["href"],
        "channel_name": feed.channel.title,
        "description": get_description(url),
        "image": feed.entries[0].media_thumbnail[0]["url"],  # most recent thumbnail
        "host": feed.channel.author,
    }


def populate_missing_youtube_fields():
    for channel in Channel.objects.all():
        if channel.youtube_url is not None:
            channel_fields = channel_dict(channel.youtube_url)
            if not channel.channel_name:
                channel.channel_name = channel_fields["channel_name"]
            if not channel.feed_href:
                channel.feed_href = channel_fields["feed_href"]
            if not channel.channel_summary:
                channel.channel_summary = channel_fields["description"]
            if not channel.channel_image:
                channel.channel_image = channel_fields["image"]
            if not channel.host:
                channel.host = channel_fields["host"]
            channel.save()


def save_new_youtube_episodes(youtube_url: str):
    """
    Checks or new episodes
    by checking if the link exists in the model already
    """
    logger.info(f"Checking for new episodes of {youtube_url}")
    feed = get_xml(youtube_url)

    channel, created = Channel.objects.get_or_create(youtube_url=youtube_url)

    for item in feed.entries:
        if not YoutubeEpisode.objects.filter(link=item.link):
            logger.info(f"Found new episodes for {channel.channel_name}")

            episode = YoutubeEpisode(
                channel_name=channel,
                title=item.title,
                description=item.summary_detail.value,
                pub_date=date_parser.parse(item.published),
                link=item.link,
                image=item.media_thumbnail[0]["url"],
            )
            logger.info(f"Added episode: {item.title}")
            episode.save()


def fetch_new_youtube_episodes():
    populate_missing_youtube_fields()
    channel_list = Channel.objects.all().filter(youtube_url__isnull=False)
    for channel in channel_list:
        youtube_url = channel.youtube_url
        logger.info(f"Getting Youtube channel {channel.channel_name}")
        save_new_youtube_episodes(youtube_url)
