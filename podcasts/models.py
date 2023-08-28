from django.db import models


class Podcast(models.Model):
    feed_href = models.URLField(unique=True)
    podcast_name = models.CharField(max_length=100)
    podcast_summary = models.TextField(null=True, blank=True)
    podcast_image = models.URLField(blank=True)
    podcast_twitter = models.URLField(unique=True, null=True, blank=True)
    host = models.TextField(null=True, blank=True)
    requires_filter = models.BooleanField(null=True)

    def __str__(self) -> str:
        return f"{self.podcast_name}"


# Create your models here.
class Episode(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    guid = models.CharField(max_length=200)
    duration = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.podcast_name}: {self.title}"


class Channel(models.Model):
    youtube_url = models.URLField(unique=True, null=True)
    feed_href = models.URLField()
    channel_name = models.CharField(max_length=100)
    channel_summary = models.TextField(null=True, blank=True)
    channel_image = models.URLField()
    channel_twitter = models.URLField(unique=True, null=True, blank=True)
    host = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.channel_name}"


class YoutubeEpisode(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    channel_name = models.ForeignKey(Channel, on_delete=models.CASCADE)
    guid = models.CharField(max_length=200)
    duration = models.CharField(max_length=10, blank=True, null=True)
