import logging
from dateutil import parser
from datetime import datetime
import feedparser
import requests

from podcasts.models import Episode, Podcast
from podcasts.parser.parse_utils import convert_duration, passes_filter

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
            if _feed.bozo:
                logger.info("Attemping to parse malformed RSS feed")
            # TODO use requests to check connection
            if not podcast.podcast_name:
                try:
                    logger.info(f"Populating {podcast.feed_href}")
                    podcast.podcast_name = _feed.channel.title
                except AttributeError as e:
                    logger.error(f"Cannot parse RSS feed. Error: {e}")

            if not podcast.podcast_summary or len(podcast.podcast_summary) < 2:
                podcast.podcast_summary = _feed.channel.get(
                    "summary", _feed.channel.get("subtitle")
                )

            if not podcast.podcast_image:
                podcast.podcast_image = _feed.channel.image["href"]
            podcast.save()


def save_episode(podcast, feed, item):
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
        fetched_date=datetime.utcnow(),
        announced_to_twitter=False,
        guid=item.guid,
    )
    logger.info(f"Episode added: {episode.title} \n")
    episode.save()


def save_new_episodes(feed):
    """Saves New episodes to database
    checks if the episode GUID against the episodes currently stored
    in the database. If not found, then a new Episode is added

    Args:
    feed: requires a feedparser object"""

    try:
        podcast, created = Podcast.objects.get_or_create(feed_href=feed.href)
        if not podcast.requires_filter:
            for item in feed.entries:
                if not Episode.objects.filter(guid=item.guid).exists():
                    logger.info(f"New episodes found for Podcast {feed.channel.title}")
                    logger.info(f"Parsing episode with GUID ${item.guid}")
                    save_episode(podcast, feed, item)

        if podcast.requires_filter:
            for item in feed.entries:
                if not Episode.objects.filter(guid=item.guid).exists():
                    if passes_filter(item):
                        save_episode(podcast, feed, item)
    except Podcast.DoesNotExist as podcastmissingexception:
        logger.info(f"Except {podcastmissingexception}")
        logger.info(
            f"Podcast URL href not found - the url has probably changed and needs to be updated or there is a network issue."
        )
    except KeyError as keyexception:
        logger.info(f"KeyException:  ${keyexception}")


def fetch_new_episodes():
    populate_missing_fields()
    """ Fetches new episodes from RSS feed"""

    podcast_list = Podcast.objects.all().filter(feed_href__isnull=False)
    for podcast in podcast_list:
        feed = podcast.feed_href
        # TODO RSS verification
        logger.info(f"Getting {feed}...")
        _feed = feedparser.parse(feed)
        if not _feed.bozo:  # todo make this like a real exception with logging
            save_new_episodes(_feed)
