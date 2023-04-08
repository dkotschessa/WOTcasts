from django.contrib import admin

# Register your models here.
from .models import Episode, Podcast


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ("id", 
                    "podcast_name")
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("podcast_name", 
                    "title",
                    "pub_date")
    
