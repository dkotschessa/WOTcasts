from django.utils import timezone

from podcasts.reports.content_report import daily_report
from podcasts.tweet_scheduler.tweet import (
    new_content_report,
    get_unannounced_episodes_and_videos,
)
import pytest

from podcasts.tests.test_parser import EpisodeFactory, PodcastFactory
from podcasts.tests.test_youtube import YoutubeEpisodeFactory, ChannelFactory
import datetime
import logging

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_daily_report():
    podcast = PodcastFactory(
        requires_filter=False,
        podcast_twitter="http://www.twitter.com/oogabooga",
    )
    channel = ChannelFactory(
        requires_filter=False, channel_twitter="http://www.twitter.com/choogabooga"
    )

    EpisodeFactory(
        pub_date=datetime.datetime.now(tz=timezone.utc),
        podcast_name=podcast,
        announced_to_twitter=False,
    )

    YoutubeEpisodeFactory(
        pub_date=datetime.datetime.now(tz=timezone.utc),
        channel_name=channel,
        announced_to_twitter=False,
    )

    output = daily_report()
    date = datetime.datetime.today().strftime("%m/%d/%Y")
    assert (
        output
        == f"\n                    Today {date}, we have new episodes from @oogabooga and @choogabooga!\n                    Check them out on www.wheeloftimepodcasts.com or\n                    in your podcast app!"
    )


@pytest.mark.django_db
def test_new_content_report():
    podcast = PodcastFactory(
        requires_filter=False,
        podcast_twitter="http://www.twitter.com/oogabooga",
    )
    channel = ChannelFactory(
        requires_filter=False, channel_twitter="http://www.twitter.com/choogabooga"
    )

    episode = EpisodeFactory(
        pub_date=datetime.datetime.now(tz=timezone.utc),
        podcast_name=podcast,
        announced_to_twitter=False,
    )

    youtubeepisode = YoutubeEpisodeFactory(
        pub_date=datetime.datetime.now(tz=timezone.utc),
        channel_name=channel,
        announced_to_twitter=False,
    )

    episodes, videos = get_unannounced_episodes_and_videos()

    # TODO separate this test
    assert episodes[0] == episode
    assert videos[0] == youtubeepisode

    output = new_content_report(episodes, videos)
    logger.info(output)
    assert "Hey" in output or "Greetings" in output or "Hi" in output
    assert "#TwitterOfTime" in output
    assert "@oogabooga" in output
    assert "@choogabooga" in output
    assert "New" in output
    assert (
        "Check them out on www.wheeloftimepodcasts.com or in your podcast app!"
        in output
    )
