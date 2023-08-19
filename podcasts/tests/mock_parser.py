from attrs import define
from typing import List, Dict
from attrs import asdict


@define
class FeedItem:
    title: str
    description: str
    published: str
    podcast_name: str
    link: str
    image: Dict[str, str]
    guid: str
    links: list

    def get(self, arg, opt_arg=None):
        feed_dict = asdict(self)
        try:
            return feed_dict[arg]
        except KeyError:
            return opt_arg


@define
class Channel:
    title: str
    summary: str
    image: str
    items: List[FeedItem]

    def get(self, arg, opt_arg=None):
        channel_dict = asdict(self)
        try:
            return channel_dict[arg]
        except KeyError:
            return opt_arg


@define
class MockFeed:
    channel: Channel
    href: str
    entries: List[FeedItem]


feeditem = FeedItem(
    title="some title",
    description="some description",
    published="Tue, 04 Apr 2023 18:30:00 -0700",
    podcast_name=Channel.title,
    image={"href": "http://www.someimagehost/img.png"},
    link="a link",
    guid="a guid",
    links=[
        {
            "length": "5",
            "type": "audio/mpeg",
            "href": "https://www.buzzsprout.com/1986660/13295473-i-don-t-know-what-a-halsey-is.mp3",
            "rel": "enclosure",
        }
    ],
)

channel = Channel(
    title="Test & Code",
    summary="Topics include automated testing, testing strategy",
    image={
        "href": "https://assets.fireside.fm/file/fireside-images/podcasts/images/b/bc7f1faf-8aad-4135-bb12-83a8af679756/cover.jpg"
    },
    items=[feeditem],
)

mock_feed = MockFeed(
    href="http://www.something.com", channel=channel, entries=[feeditem]
)
