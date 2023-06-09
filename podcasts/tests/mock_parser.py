from attrs import define
from typing import List

@define
class FeedItem:
    title: str
    description: str
    published: str
    podcast_name: str
    link: str
    image: str
    guid: str
    


@define
class Channel:
    title: str
    summary: str
    image: str
    items: List[FeedItem]

@define
class MockFeed:
    channel: Channel
    href: str
    entries: List[FeedItem]

feeditem = FeedItem(
    title = "some title",
    description="some description",
    published = 'Tue, 04 Apr 2023 18:30:00 -0700',
    podcast_name = Channel.title,
    image = "",
    link = "a link",
    guid = "a guid"
)

channel = Channel(
    title = "Test & Code",
    summary= "Topics include automated testing, testing strategy",
    image = {"href" : "https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover.jpg"},
    items = [feeditem]
)

mock_feed = MockFeed(href = "http://www.something.com", channel=channel, entries = [feeditem])

