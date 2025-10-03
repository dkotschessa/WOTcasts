import factory

from podcasts.models import Channel, YoutubeEpisode, Podcast, Episode
from faker import Faker

fake = Faker()


class ChannelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Channel

    channel_name = "Great youtube channel"

    youtube_url = fake.url()


class YoutubeEpisodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = YoutubeEpisode

    title = "Another amazing video"
    pub_date = fake.date()
    link = fake.url()
    image = fake.url()
    guid = fake.url()
    channel_name = factory.SubFactory(ChannelFactory, youtube_url=fake.url())
    duration = "1022"
    announced_to_twitter = True


class PodcastFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Podcast

    podcast_name = "Amazing podcast"
    feed_href = "http://podcast1.com"


class EpisodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Episode

    title = fake.sentence()
    description = fake.sentence()
    pub_date = fake.date()
    link = fake.url()
    duration = "1000"
    announced_to_twitter = "False"

    guid = fake.uuid4()

    podcast_name = factory.SubFactory(PodcastFactory, feed_href=fake.url())
