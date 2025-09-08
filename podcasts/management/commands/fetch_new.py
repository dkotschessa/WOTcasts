import logging

from django.core.management import BaseCommand
from podcasts.parser.episode_parser import fetch_new_episodes
from podcasts.parser.youtube_parser import fetch_new_youtube_episodes
import logging

from django.core.management import BaseCommand
from podcasts.parser.episode_parser import fetch_new_episodes
from podcasts.parser.youtube_parser import fetch_new_youtube_episodes

logger = logging.getLogger("wotcasts.aggregator")


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
