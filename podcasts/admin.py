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
    fields = [
        "podcast_name",
        "feed_href",
        "podcast_image",
        "podcast_twitter",
        "requires_filter",
    ]
    list_filter = ("feed_href", "podcast_name", "requires_filter")
    search_fields = (
        "podcast_name__startswith",
        "feed_href__startswith",
    )


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
    list_filter = ("podcast_name", "pub_date")
    search_fields = ("podcast_podcast_name__startswith", "title__startswith")


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = [
        "youtube_url",
        "feed_href",
        "channel_name",
        "channel_summary",
        "host",
    ]
    list_filter = ("channel_name",)

    fields = ["youtube_url", "channel_twitter", "requires_filter"]
    search_fields = ("youtube_url__startswith", "channel_channel_name__startswith")


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
    list_filter = ("channel_name", "pub_date")
    search_fields = ("channel_name__startswith", "title__startswith")
