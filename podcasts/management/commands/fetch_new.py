import logging


from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings
from podcasts.models import Episode
from django.core.management import BaseCommand
from podcasts.parser.episode_parser import fetch_new_episodes


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):

        logger.info("Attempting to fetch new episodes")

        try:
            fetch_new_episodes()

        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")
