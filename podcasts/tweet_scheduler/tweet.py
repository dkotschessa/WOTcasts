import tweepy
from os import environ
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import logging

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

# client.create_tweet(msg)
