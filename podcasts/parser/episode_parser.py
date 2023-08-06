import logging
from typing import List
from dateutil import parser
import feedparser

from podcasts.models import Episode, Podcast
from podcasts.parser.parse_utils import convert_duration

logger = logging.getLogger(__name__)


def populate_missing_fields():
    """
    Populate fields that are missing
    mostly used when new podcast is added
    """

    for podcast in Podcast.objects.all():
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


def save_new_episodes(feed):
    """Saves New episodes to database
    checks if the wpisode GUID against the episodes currently stored
    in the datebase. If not found, then a new Episode is added

    Args:
    feed: requires a feedparser object"""

    logger.info("Checking for new episodes...")

    try:
        podcast, created = Podcast.objects.get_or_create(feed_href=feed.href)
    except AttributeError as attributeerror:
        logger.info(f"Attribute Error:  ${attributeerror}")
    except KeyError as keyexception:
        logger.info(f"KeyException:  ${keyexception}")

    for item in feed.entries:
        if not Episode.objects.filter(guid=item.guid).exists():
            logger.info(f"New episodes found for Podcast {feed.channel.title}")
            logger.info(f"Parsing episode with GUID ${item.guid}")
            episode = Episode(
                title=item.title,
                description=item.get("description", ""),
                pub_date=parser.parse(item.published),
                link=item.get("link", item.links[0]["href"]),
                podcast_name=podcast,  ##TODO not sure what's up here
                image=podcast.podcast_image,
                duration=convert_duration(item.itunes_duration),
                guid=item.guid,
            )
            logger.info(f"Episode added: {episode.title} \n")
            episode.save()


def get_rss_feed_list() -> List:
    podcast_list = Podcast.objects.all().filter(feed_href__isnull=False)
    # TODO check is actually RSS feed
    return [p.feed_href for p in podcast_list]


def fetch_new_episodes():
    populate_missing_fields()
    """ Fetches new episodes from RSS feed"""
    feeds = get_rss_feed_list()
    for feed in feeds:
        logger.info(f"Getting {feed}...")
        _feed = feedparser.parse(feed)
        save_new_episodes(_feed)
