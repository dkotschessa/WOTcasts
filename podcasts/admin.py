from django.contrib import admin

# Register your models here.
from .models import Episode, Podcast, Channel, YoutubeEpisode


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "feed_href",
        "podcast_name",
        "podcast_summary",
        "podcast_image",
        "host",
        "requires_filter",
    )
    fields = ["feed_href", "podcast_image", "podcast_twitter", "requires_filter"]


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        "podcast_name",
        "title",
        "pub_date",
        "link",
        "image",
        "duration",
        "guid",
    )


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = [
        "youtube_url",
        "feed_href",
        "channel_name",
        "channel_summary",
        "host",
    ]

    fields = ["youtube_url", "channel_twitter"]


@admin.register(YoutubeEpisode)
class YoutubeEpisodeAdmin(admin.ModelAdmin):
    list_display = [
        "channel_name",
        "title",
        "description",
        "pub_date",
        "link",
        "image",
        "guid",
        "duration",
    ]
