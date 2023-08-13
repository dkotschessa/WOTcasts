from typing import Dict
from feedparser.util import FeedParserDict
from dateutil import parser as date_parser

import requests
from bs4 import BeautifulSoup
import feedparser
from podcasts.models import Channel, YoutubeEpisode
import logging

logger = logging.getLogger(__name__)

test_urls = [
    "https://www.youtube.com/@TotalRunningProductions",
    "https://www.youtube.com/@Grazzyy",
    "https://www.youtube.com/@MarkLewisfitness",
    "https://www.youtube.com/@middick",
    "https://www.youtube.com/@WebDevSimplified",
]


def soup_tube(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_rss_from_channel(url):
    soup = soup_tube(url)
    feed_href = soup.find(title="RSS")
    return feed_href["href"]


def get_xml(url):
    feed_href = get_rss_from_channel(url)
    feed = feedparser.parse(feed_href)
    return feed


def get_description(url):
    soup = soup_tube(url)
    og_description = soup.find("meta", property="og:description")
    description = og_description.get("content")
    return description


def channel_dict(url) -> Dict:
    feed = get_xml(url)

    return {
        "feed_href": feed.channel.links[0]["href"],
        "channel_name": feed.channel.title,
        "description": get_description(url),
        "image": feed.entries[0].media_thumbnail[0]["url"],  # most recent thumbnail
        "host": feed.channel.author,
    }


def episode_dict(episode: FeedParserDict) -> Dict:
    title = episode.title
    description = episode.summary_detail.value
    pub_date = date_parser.parse(episode.published)
    link = episode.links[0].href
    image = episode.media_thumbnail[0]["url"]
    guid = episode.guid

    return {
        "title": title,
        "description": description,
        "pub_date": pub_date,
        "link": link,
        "image": image,
        "guid": guid,
    }


def populate_missing_youtube_fields():
    """
    Populate fields that are missing
    mostly used when new podcast is added
    """

    for podcast in Chann.objects.all():
        if podcast.feed_href is not None:
            rss_link = podcast.feed_href
            _feed = feedparser.parse(rss_link)
            if not podcast.podcast_name:
                podcast.podcast_name = _feed.channel.title
                # todo maybe a separate function for this with error handling

            if not podcast.podcast_summary or len(podcast.podcast_summary) < 2:
                podcast.podcast_summary = _feed.channel.get(
                    "summary", _feed.channel.get("subtitle")
                )

            if not podcast.podcast_image:
                podcast.podcast_image = _feed.channel.image["href"]
            podcast.save()


def save_new_youtube_episodes(feed):
    """Saves New youtube episodes to database
    checks if the episode GUID against the episodes currently stored
    in the database. If not found, then a new Episode is added

    Args:
    feed: requires a feedparser object"""

    logger.info(f"Checking for new youtube episodes of {feed.channel.title}")

    try:
        podcast, created = Channel.objects.get_or_create(feed_href=feed.href)
    except AttributeError as attributeerror:
        logger.info(f"Attribute Error:  ${attributeerror}")
    except KeyError as keyexception:
        logger.info(f"KeyException:  ${keyexception}")

    for item in feed.entries:
        if not Channel.objects.filter(guid=item.guid).exists():
            logger.info(f"New episodes found for Podcast {feed.channel.title}")
            logger.info(f"Parsing episode with GUID ${item.guid}")
            episode = Episode(
                title=item.title,
                description=item.get("description", ""),
                pub_date=parser.parse(item.published),
                link=item.get("link", item.links[0]["href"]),
                podcast_name=podcast,  ##TODO not sure what's up here
                image=podcast.podcast_image,
                duration=convert_duration(item.get("itunes_duration", "N/A")),
                guid=item.guid,
            )
            logger.info(f"Episode added: {episode.title} \n")
            episode.save()


def fetch_new_youtube_episodes():
    populate_missing_fields()
    """ Fetches new episodes from RSS feed"""
    feeds = get_rss_feed_list()
    for feed in feeds:
        logger.info(f"Getting {feed}...")
        _feed = feedparser.parse(feed)
        save_new_episodes(_feed)
