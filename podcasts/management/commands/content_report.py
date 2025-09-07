import logging

from django.core.management import BaseCommand
from podcasts.reports.content_report import save_report_to_file

logger = logging.getLogger("wotcasts.aggregator")


class Command(BaseCommand):
    def add_arguments(self, report):
        report.add_argument(
            "days",
            type=int,
            help="Number of days back for report",
        )

    def handle(self, *args, **options):
        days = options["days"]

        logger.info("creating daily report")

        try:
            save_report_to_file(days)

        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")
