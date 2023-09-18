import logging

from django.core.management import BaseCommand
from podcasts.tweet_scheduler.tweet import tweet_new_episodes

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):

        logger.info("Checking if there's any new episodes to tweet")

        try:
            tweet_new_episodes()

        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")
