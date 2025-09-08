from podcasts.tweet_scheduler.tweet import (
    tweet_new_episodes,
    get_unannounced_episodes_and_videos,
)

import logging

from django.core.management import BaseCommand
from podcasts.parser.episode_parser import fetch_new_episodes
from podcasts.parser.youtube_parser import fetch_new_youtube_episodes

logger = logging.getLogger("wotcasts.aggregator")


def fetch_and_tweet_content():
    logger.info("Fetching new podcast episodes")
    fetch_new_episodes()
    logger.info("Fetching new youtube episodes")
    fetch_new_youtube_episodes()
    logger.info("Checking if anything needs to bet tweeted")
    tweet_new_episodes()


class Command(BaseCommand):
    def handle(self, *args, **options):

        logger.info("Attempting to fetch new episodes")

        try:
            fetch_and_tweet_content()

        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")
