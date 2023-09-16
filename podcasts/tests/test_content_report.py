from django.utils import timezone

from podcasts.reports.content_report import daily_report
import pytest

from podcasts.tests.test_parser import EpisodeFactory, PodcastFactory
from podcasts.tests.test_youtube import YoutubeEpisodeFactory, ChannelFactory
import datetime


@pytest.mark.django_db
def test_daily_report():
    podcast = PodcastFactory(
        requires_filter=False, podcast_twitter="http://www.twitter.com/oogabooga"
    )
    channel = ChannelFactory(
        requires_filter=False, channel_twitter="http://www.twitter.com/choogabooga"
    )

    EpisodeFactory(
        pub_date=datetime.datetime.now(tz=timezone.utc), podcast_name=podcast
    )

    YoutubeEpisodeFactory(
        pub_date=datetime.datetime.now(tz=timezone.utc), channel_name=channel
    )

    output = daily_report()
    assert (
        output
        == "\n                    Today 09/08/2023, we have new episodes from @oogabooga and @choogabooga!\n                    Check them out on www.wheeloftimepodcasts.com or\n                    in your podcast app!"
    )
