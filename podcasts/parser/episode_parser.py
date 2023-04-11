
import logging
from typing import List
from dateutil import parser
import feedparser

from podcasts.models import Episode, Podcast

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
            if not podcast.podcast_summary:
                 podcast.podcast_summary = _feed.channel.summary
            if not podcast.podcast_image:
                podcast.podcast_image = _feed.channel.image["href"]
            podcast.save()

def save_new_episodes(feed):
    """ Saves New episodes to database
    checks if the wpisode GUID against the episodes currently stored
    in the datebase. If not found, then a new Episode is added 
    
    Args: 
    feed: requires a feedparser object"""

    logger.info("Checking for new episodes...")

    podcast, created =  Podcast.objects.get_or_create(feed_href = feed.href)
   
    for item in feed.entries:
             
        if not Episode.objects.filter(guid = item.guid).exists():
            logger.info(f"New episodes found for Podcast {feed.channel.title}")
            episode = Episode(title = item.title, 
                                description = item.description,
                                pub_date = parser.parse(item.published),
                                link = item.link,
                                podcast_name = podcast,
                                image = item.image['href'],
                                guid = item.guid)
            episode.save()


def get_rss_feed_list() -> List:
     podcast_list = Podcast.objects.all().filter(feed_href__isnull=False)
     return [p.feed_href for p in podcast_list]
     


def fetch_new_episodes():
      populate_missing_fields()
      """ Fetches new episodes from RSS feed"""
      feeds = get_rss_feed_list()
      for feed in feeds:
            _feed = feedparser.parse(feed)
            save_new_episodes(_feed)
      