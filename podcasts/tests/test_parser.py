
import logging
from typing import List

import feedparser
from podcasts.parser.episode_parser import populate_missing_fields
from dateutil import parser

from podcasts.models import Episode, Podcast



class PodcastTests(TestCase):
    def setUp(self):
        self.podcast = Podcast.objects.create(
                                              feed_href = "http://something.rss/")
                