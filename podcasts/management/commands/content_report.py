import logging

from django.core.management import BaseCommand
from podcasts.reports.content_report import save_report_to_file

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):

        logger.info("Attempting to fetch new episodes")

        try:
            save_report_to_file()

        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")
