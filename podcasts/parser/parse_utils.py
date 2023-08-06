import datetime
import logging
import feedparser

from podcasts.models import Episode, Podcast

logger = logging.getLogger(__name__)


def convert_duration(duration: str):
    logger.info("Checking episode duration")
    if ":" in duration:  # regular format
        logger.info("Duration is already in proper format")
        return duration
    else:  # duration is in seconds
        logger.info(f"Duration listed as {duration} seconds. Converting.")
        seconds = int(duration)
        converted_duration = datetime.timedelta(seconds=seconds)
        logger.info(f"Converting to {converted_duration}")
        return str(converted_duration)


def episode_rss_lookup(episode: Episode):
    """
    For an episode in the DB, find it's entry in RSS
    Return its complete RSS entry
    """
    podcast = Podcast.objects.get(episode__guid=episode.guid)
    feed_href = podcast.feed_href
    feed = feedparser.parse(feed_href)
    for item in feed.entries:
        if item.guid == episode.guid:
            return item
    return None


def populate_missing_episode_duration(episode: Episode):
    """
    get episode duration from RSS and save to model
    """
    logger.info(f"Looking up duration for{episode.title}")
    rss_fields = episode_rss_lookup(episode)
    duration = convert_duration(rss_fields.itunes_duration)
    episode.duration = duration
    episode.save()
    logger.info(f"Duration saved as {duration}")
