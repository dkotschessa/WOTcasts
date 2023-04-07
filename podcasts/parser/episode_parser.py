
import logging

import feedparser
from dateutil import parser

from podcasts.models import Episode, Podcast
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)





def save_new_episodes_raw_data(feed):
    """ Saves New episodes to database
    checks if the wpisode GUID against the episodes currently stored
    in the datebase. If not found, then a new Episode is added 
    
    Args: 
    feed: requires a feedparser object"""

    podcast_title = feed.channel.title
    podcast_image = feed.channel.image["href"]
    logger.info("Checking for new episodes...")

          
    for item in feed.entries:
        if not Episode.objects.filter(guid = item.guid).exists():
            logger.info(f"New episodes found for Podcast {podcast_title}")
            podcast = Podcast(podcast_name = podcast_title)
            podcast.save()
            episode = Episode(title = item.title, 
                                description = item.description,
                                pub_date = parser.parse(item.published),
                                link = item.link,
                                podcast_name = podcast,
                                image = podcast_image,
                                guid = item.guid)
            episode.save()



def fetch_the_wheel_weaves():
        """ Fetches new episodes from RSS for the Wheel Weaves podcast"""
        _feed = feedparser.parse("https://www.spreaker.com/show/5482260/episodes/feed")
        save_new_episodes_raw_data(_feed)

def fetch_the_dragon_reread():
        """ Fetches new episodes from RSS for The Dragon ReRead podcast"""
        _feed = feedparser.parse("https://thedragonreread.com/rss")
        save_new_episodes_raw_data(_feed)
