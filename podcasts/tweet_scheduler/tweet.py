import random

import tweepy
from os import environ
from dotenv import load_dotenv
import logging

from podcasts.models import Episode, YoutubeEpisode
from podcasts.reports.content_report import (
    get_podcasts_channels_from_episode_list,
    get_twitter_tags,
)

load_dotenv()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

API_KEY = environ["API_KEY"]
API_SECRET_KEY = environ["API_SECRET_KEY"]
ACCESS_TOKEN = environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = environ["ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = environ["BEARER_TOKEN"]

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

msg = "test tweet"


def set_content_announcement_flag_true(episodes, videos):
    if episodes.exists():
        for episode in episodes:
            episode.announced_to_twitter = True
            episode.save()
    if videos.exists():
        for video in videos:
            video.announced_to_twitter = True
            video.save()


def tweet_new_episodes():
    logger.info("Checking for any unnannounced episodes")
    episodes, videos = get_unannounced_episodes_and_videos()
    if episodes.exists():
        logging.info(f"Unannounced episodes to tweet: {episodes} ")
    if videos.exists():
        logging.info(f"Unannounced videos to tweet: {videos} ")

    if episodes.exists() or videos.exists():
        logging.info("tweeting content")
        tweet = new_content_report(episodes, videos)
        logger.info(f"Attempting to send tweet: {tweet}")
        response = client.create_tweet(text=tweet)

        if not response.errors:

            set_content_announcement_flag_true(episodes, videos)
        else:
            logging.info(f"Errors when tweeting: {response.errors}")
    else:
        logger.info("no new content")


def get_unannounced_episodes_and_videos():
    episodes = Episode.objects.filter(announced_to_twitter=False)

    videos = YoutubeEpisode.objects.filter(announced_to_twitter=False)
    return episodes, videos


def new_content_report(episodes, videos):
    podcasts, channels = get_podcasts_channels_from_episode_list(episodes, videos)

    tags = get_twitter_tags(podcasts, channels)

    # TODO morning afternoon evening
    greeting = random.choice(
        [
            "Hey #TwitterOfTime! ",
            "Hey there #TwitterOfTime! ",
            "Greetings #TwitterOfTime! ",
            "Hi #TwitterOfTime! ",
            "Hey #TwitterOfTime! ",
        ]
    )
    content_announcement = random.choice(
        [
            "New stuff from: ",
            "New content from: ",
            "New episodes from: ",
        ]
    )
    content = []
    for episode in episodes:
        content.append(f"{episode.podcast_name}: {episode.title}\n")
    for video in videos:
        content.append(f"{video.channel_name}: {video.title}\n")

    footer = "Check them out on www.wheeloftimepodcasts.com or in your podcast app!"
    short_format = (
        greeting + "\n" + content_announcement + tags + "!" + "\n" + "".join(content)
    )
    long_format = short_format + footer
    if len(long_format) > 280:
        return short_format
    else:
        return long_format
