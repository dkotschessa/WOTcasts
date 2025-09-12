import datetime

import pytest
from datetime import timezone

from podcasts.tests.test_content_report import logger
from podcasts.tests.factories import (
    ChannelFactory,
    YoutubeEpisodeFactory,
    PodcastFactory,
    EpisodeFactory,
)
from podcasts.tweet_scheduler.tweet import (
    get_unannounced_episodes_and_videos,
    new_content_report,
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
        title="a cool episode",
        podcast_name=podcast,
        announced_to_twitter=False,
    )

    youtubeepisode = YoutubeEpisodeFactory(
        pub_date=datetime.datetime.now(tz=timezone.utc),
        title="A great video",
        channel_name=channel,
        announced_to_twitter=False,
    )

    episodes, videos = get_unannounced_episodes_and_videos()

    # TODO separate this test
    assert episodes[0] == episode
    assert videos[0] == youtubeepisode

    output = new_content_report(episodes, videos)
    assert "Hey" in output or "Greetings" in output or "Hi" in output
    assert "#TwitterOfTime" in output
    assert "@oogabooga" in output
    assert "@choogabooga" in output
    assert "new" in output.lower()
    assert (
        "Check them out on www.wheeloftimepodcasts.com or in your podcast app!"
        in output
    )


@pytest.mark.django_db
def test_new_content_report_no_twitter_tags():
    podcast = PodcastFactory(
        requires_filter=False,
    )
    channel = ChannelFactory(
        requires_filter=False,
    )

    episode = EpisodeFactory(
        pub_date=datetime.datetime.now(tz=timezone.utc),
        title="a cool episode",
        podcast_name=podcast,
        announced_to_twitter=False,
    )

    youtubeepisode = YoutubeEpisodeFactory(
        pub_date=datetime.datetime.now(tz=timezone.utc),
        title="A great video",
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
    assert "Amazing podcast and Great youtube channel!" in output
    assert "new" in output.lower()
    assert (
        "Check them out on www.wheeloftimepodcasts.com or in your podcast app!"
        in output
    )
