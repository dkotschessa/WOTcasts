import datetime
import os
from podcasts.models import Episode, YoutubeEpisode
from pathlib import Path
from content_aggregator.settings.base import BASE_DIR


def get_todays_content():
    episodes = Episode.objects.filter(pub_date__gte=datetime.datetime.today().date())
    videos = YoutubeEpisode.objects.filter(
        pub_date__gte=datetime.datetime.today().date()
    )

    return episodes, videos


def get_podcasts_and_channels_to_be_mentioned():
    episodes, videos = get_todays_content()

    podcasts = set([episode.podcast_name for episode in episodes])
    channels = set([video.channel_name for video in videos])

    return podcasts, channels


def get_podcast_and_channel_names():
    podcasts, channels = get_podcasts_and_channels_to_be_mentioned()

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


def get_twitter_tag(twitter_url):
    twitter_tag = twitter_url.split("/")[-1]
    return f"@{twitter_tag}"


def get_twitter_tags_and_return_string():
    podcasts, channels = get_podcasts_and_channels_to_be_mentioned()

    # get Twitter Tags
    twitter_tags = []
    for podcast in podcasts:
        if podcast.podcast_twitter:
            twitter_tags.append(get_twitter_tag(podcast.podcast_twitter))
    for channel in channels:
        if channel.channel_twitter:
            twitter_tags.append(get_twitter_tag(channel.channel_twitter))

    all_tags_but_last = twitter_tags[:-1]
    last_name = twitter_tags[-1]

    # nice comma separated string for reporting
    tags = ", ".join(all_tags_but_last) + " and " + last_name

    return tags


def daily_report():
    # TODOS
    # randomize header, twitter tag, phrasing to make less repetitive
    date = datetime.datetime.today().strftime("%m/%d/%Y")

    tag_string = get_twitter_tags_and_return_string()
    report_string = f"""
                    Today {date}, we have new episodes from {tag_string}!
                    Check them out on www.wheeloftimepodcasts.com or
                    in your podcast app!"""
    return report_string


def save_report_to_file():
    reports_dir = BASE_DIR / "reports"
    date = datetime.datetime.today().strftime("%m-%d-%Y")
    report_file = reports_dir / f"report_{date}"

    with open(report_file, "w") as file:
        file.write(daily_report())
    file.close()
