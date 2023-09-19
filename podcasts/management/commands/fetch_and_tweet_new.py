from podcasts.tweet_scheduler.tweet import (
    tweet_new_episodes,
    get_unannounced_episodes_and_videos,
)

import logging

from django.core.management import BaseCommand
from podcasts.parser.episode_parser import fetch_new_episodes
from podcasts.parser.youtube_parser import fetch_new_youtube_episodes

logger = logging.getLogger(__name__)


def fetch_and_tweet_content():
    fetch_new_episodes()
    fetch_new_youtube_episodes()
    tweet_new_episodes()


class Command(BaseCommand):
    def handle(self, *args, **options):

        logger.info("Attempting to fetch new episodes")

        try:
            fetch_and_tweet_content()

        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")


logger = logging.getLogger(__name__)


def fetch_all_content():
    fetch_new_episodes()
    fetch_new_youtube_episodes()


class Command(BaseCommand):
    def handle(self, *args, **options):

        logger.info("Attempting to fetch new episodes")

        try:
            fetch_all_content()

        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")
