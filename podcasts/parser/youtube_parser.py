from typing import Dict

import requests
from bs4 import BeautifulSoup
import feedparser

test_urls = [
    "https://www.youtube.com/@TotalRunningProductions",
    "https://www.youtube.com/@Grazzyy",
    "https://www.youtube.com/@MarkLewisfitness",
    "https://www.youtube.com/@middick",
    "https://www.youtube.com/@WebDevSimplified",
]


def soup_tube(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_rss_from_channel(url):
    soup = soup_tube(url)
    feed_href = soup.find(title="RSS")
    return feed_href["href"]


def get_xml(url):
    feed_href = get_rss_from_channel(url)
    feed = feedparser.parse(feed_href)
    return feed


def get_description(url):
    soup = soup_tube(url)
    og_description = soup.find("meta", property="og:description")
    description = og_description.get("content")
    return description


def get_elements(url) -> Dict:
    feed = get_xml(url)

    element_dict = {
        "feed_href": get_xml(url),
        "channel_name": feed.channel.title,
        "description": get_description(url),
    }
