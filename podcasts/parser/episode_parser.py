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
    checks if the episode GUID against the episodes currently stored
    in the database. If not found, then a new Episode is added

    Args:
    feed: requires a feedparser object"""

    logger.info(f"Checking for new episodes of {feed.channel.title}")

    try:
        podcast, created = Podcast.objects.get_or_create(feed_href=feed.href)
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
                # Image may unique to each episode, otherwise get podcast image
                # https://podcasters.apple.com/support/896-artwork-requirements
                image=item.get("image", feed.channel.image)["href"],
                duration=convert_duration(item.get("itunes_duration", "N/A")),
                guid=item.guid,
            )
            logger.info(f"Episode added: {episode.title} \n")
            episode.save()


def fetch_new_episodes():
    populate_missing_fields()
    """ Fetches new episodes from RSS feed"""
    podcast_list = Podcast.objects.all().filter(feed_href__isnull=False)
    for podcast in podcast_list:
        feed = podcast.feed_href
        # TODO RSS verification
        logger.info(f"Getting {feed}...")
        _feed = feedparser.parse(feed)
        save_new_episodes(_feed)
