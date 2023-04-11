from attrs import define
from typing import List

@define
class FeedItem:
    description: str
    published: str
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

feeditem = FeedItem(
    description="some description",
    published = "a date",
    link = "a link",
    image = "an image url",
    guid = "a guid"

)

channel = Channel(
    title = "Test & Code",
    summary= "Topics include automated testing, testing strategy",
    image = {"href" : "https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover.jpg"},
    items = [feeditem]
)

mock_feed = MockFeed(channel=channel)