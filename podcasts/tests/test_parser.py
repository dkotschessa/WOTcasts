
import logging
from collections import namedtuple
from typing import List
from django.test import TestCase
import feedparser
from podcasts.parser.episode_parser import populate_missing_fields
from dateutil import parser
from unittest.mock import patch
from podcasts.models import Episode, Podcast

    


class PodcastTests(TestCase):
    def setUp(self): #TODO factory
        Podcast.objects.create(
                                              feed_href = "https://feeds.fireside.fm/testandcode/rss")
    
    def test_populate_missing_fields(self):
        with patch('podcasts.parser.episode_parser.feedparser.parse') as mock_parse:
            mock_parse.return_value = test_feed
            populate_missing_fields() #TODO mock feedparser
            podcast = Podcast.objects.last()
            assert podcast.podcast_name == "Test & Code"
            assert "Topics include automated testing, testing strategy" in podcast.podcast_summary
            assert podcast.podcast_image== "https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover.jpg"



        
        

        
                