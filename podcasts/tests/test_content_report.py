from django.utils import timezone

from podcasts.reports.content_report import daily_report, get_twitter_tags
import pytest

from podcasts.tests.factories import (
    ChannelFactory,
    YoutubeEpisodeFactory,
    PodcastFactory,
    EpisodeFactory,
)
import datetime
import logging

logger = logging.getLogger("wotcasts.aggregator")


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
def test_get_twitter_tags():
    podcast = PodcastFactory(
        requires_filter=False,
        podcast_twitter="http://www.twitter.com/oogabooga",
    )
    channel = ChannelFactory(
        requires_filter=False, channel_twitter="http://www.twitter.com/choogabooga"
    )
    tags = get_twitter_tags([podcast], [channel])
    assert tags == "@oogabooga and @choogabooga"


@pytest.mark.django_db
def test_get_twitter_tags_single_name():
    podcast = PodcastFactory(
        requires_filter=False,
        podcast_twitter="http://www.twitter.com/oogabooga",
    )
    channel = ChannelFactory(requires_filter=False)
    tags = get_twitter_tags([podcast], [channel])
    assert tags == "@oogabooga"
