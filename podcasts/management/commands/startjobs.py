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


def delete_old_job_executions(max_age = 604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)



class Command(BaseCommand):
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone = settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_new_episodes,
            trigger = "interval",
            minutes = 2,
            id = "Fetch New Podcast Episodes",
            max_instances = 1,
            replace_existing=True
        )
        logger.info("Added job: Fetch new episodes")

        try:
            logger.info("Starting Scheduler")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully")


