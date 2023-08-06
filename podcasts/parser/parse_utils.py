import datetime
import logging
import feedparser

from podcasts.models import Episode, Podcast

logger = logging.getLogger(__name__)


def convert_duration(duration: str):
    if duration == "N/A":
        return duration
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
    logger.info(
        f"looking up rss feed for guid {feed_href} for podcast {podcast.podcast_name}"
    )
    feed = feedparser.parse(feed_href)
    for item in feed.entries:
        if item.guid == episode.guid:
            logger.info(f"Found episode {episode.title}")
            return item
    return None


def populate_missing_episode_duration(episode: Episode):
    """
    get episode duration from RSS and save to model
    """
    logger.info(f"Looking up duration for{episode.title}")
    rss_fields = episode_rss_lookup(episode)
    try:
        itunes_duration = rss_fields.itunes_duration
    except AttributeError:
        logger.info(f"Missing duration field in RSS for {episode.title}")
        itunes_duration = "N/A"
    duration = convert_duration(itunes_duration)
    episode.duration = duration
    episode.save()
    logger.info(f"Duration saved as {duration}")
