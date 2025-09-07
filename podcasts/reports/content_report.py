import datetime

from podcasts.models import Episode, YoutubeEpisode
from content_aggregator.settings.base import BASE_DIR
from django.utils import timezone

from podcasts.utils.helpers import get_twitter_tag
import logging

logger = logging.getLogger("wotcasts.aggregator")


def get_podcasts_channels_from_episode_list(episodes, videos):
    podcasts = set([episode.podcast_name for episode in episodes])
    channels = set([video.channel_name for video in videos])

    return podcasts, channels


def get_podcasts_channels_by_days_ago(days=0):
    days_ago = datetime.timedelta(days=days)
    episodes = Episode.objects.filter(
        pub_date__date__gte=datetime.datetime.now(tz=timezone.utc) - days_ago
    )

    videos = YoutubeEpisode.objects.filter(
        pub_date__date__gte=datetime.datetime.now(tz=timezone.utc) - days_ago
    )

    podcasts, channels = get_podcasts_channels_from_episode_list(episodes, videos)
    return podcasts, channels


def get_podcast_and_channel_names():
    podcasts, channels = get_podcasts_channels_by_days_ago()

    # Get the podcast and channel names themselves
    podcast_names = [podcast.podcast_name for podcast in podcasts]
    channel_names = [channel.channel_name for channel in channels]

    return podcast_names, channel_names


def combine_names_and_return_string():
    podcast_names, channel_names = get_podcast_and_channel_names()

    all_names = podcast_names + channel_names
    all_names_but_last = all_names[:-1]
    last_name = all_names[-1]

    # nice comma separated string for reporting
    names_string = ", ".join(all_names_but_last) + " and " + last_name

    return names_string


def get_twitter_tags(podcasts, channels):
    # get Twitter Tags

    twitter_tags = []
    for podcast in podcasts:
        if podcast.podcast_twitter:
            twitter_tags.append(get_twitter_tag(podcast.podcast_twitter))
    for channel in channels:
        if channel.channel_twitter:
            twitter_tags.append(get_twitter_tag(channel.channel_twitter))

    if len(twitter_tags) == 1:
        tags = twitter_tags[0]
    else:
        all_tags_but_last = twitter_tags[:-1]
        last_name = twitter_tags[-1]
        if len(twitter_tags) == 1:
            return last_name
        # nice comma separated string for reporting
        tags = ", ".join(all_tags_but_last) + " and " + last_name
    return tags


def get_twitter_tags_and_return_string(days=0):
    podcasts, channels = get_podcasts_channels_by_days_ago(days)

    return get_twitter_tags(podcasts, channels)


def daily_report(days=0):
    # TODOS
    # randomize header, twitter tag, phrasing to make less repetitive
    date = datetime.datetime.today().strftime("%m/%d/%Y")

    tag_string = get_twitter_tags_and_return_string(days)
    report_string = f"""
                    Today {date}, we have new episodes from {tag_string}!
                    Check them out on www.wheeloftimepodcasts.com or
                    in your podcast app!"""
    shorter_format = f"""
                     Today {date}, we have new episodes from {tag_string}!
                     """
    shortest_format = f"""
                     New content from {tag_string}!"""
    if len(report_string) > 279:
        report_string = shorter_format
    if len(shorter_format) > 279:
        report_string = shortest_format
    if len(shortest_format) > 279:
        logger.info("Tweet format exceeds twitter limit")
        return None
    return report_string


def save_report_to_file(days=0):
    reports_dir = BASE_DIR / "reports"
    date = datetime.datetime.today().strftime("%m-%d-%Y")
    report_file = reports_dir / f"report_{date}"
    logger.info(f"saving report for {days} days to {report_file}")

    with open(report_file, "w") as file:
        file.write(str(daily_report(days)))
    file.close()
