import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings
from django.core.management import BaseCommand
from fetch_new import fetch_all_content

logger = logging.getLogger(__name__)


def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "interval",
            type=int,
            help="Indicates number of minutes to wait between fetching",
        )

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        interval = options["interval"]

        scheduler.add_job(
            fetch_all_content,
            trigger="interval",
            minutes=interval,
            id="Fetch New Podcast and Youtube Episodes",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(f"Added job: Fetch new episodes every {interval} minutes")

        try:
            logger.info("Starting Scheduler")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully")
