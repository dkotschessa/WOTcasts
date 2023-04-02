import logging

import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings
from podcasts.models import Episode
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)

def save_new_episodes(feed):
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
            episode = Episode(title = item.title, 
                                description = item.description,
                                pub_date = parser.parse(item.published),
                                link = item.link,
                                image = podcast_image,
                                podcast_name = podcast_title,
                                guid = item.guid)
            episode.save()


def fetch_realpython_episodes():
    """ Fetches new episodes from RSS for the Realpython podcast"""
    _feed = feedparser.parse("https://realpython.com/podcasts/rpp/feed")
    save_new_episodes(_feed)


def fetch_talkpython_episodes():
    """ Fetches new episodes from RSS for the Talk Python podcast
    """
    _feed = feedparser.parse("https://talkpython.fm/episodes/rss")
    save_new_episodes(_feed)

def delete_old_job_executions(max_age = 604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)




class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone = settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_realpython_episodes,
            trigger = "interval",
            minutes = 2,
            id = "The Real Python Podcast",
            max_instances = 1,
            replace_existing=True
        )
        logger.info("Added job: The Real Python Podcast")

        scheduler.add_job(
            fetch_talkpython_episodes,
            trigger="interval",
            minutes=2,
            id="Talk Python Feed",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: Talk Python Feed.")

        try:
            logger.info("Starting Scheduler")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully")


