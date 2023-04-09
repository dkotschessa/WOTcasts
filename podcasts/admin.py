from django.contrib import admin

# Register your models here.
from .models import Episode, Podcast


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ("id",
                    "feed_href", 
                    "podcast_name",
                    "podcast_summary",
                    "podcast_image")
    fields = ["feed_href"]
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("podcast_name", 
                    "title",
                    "pub_date")
    
