from rest_framework import serializers

from podcasts.models import Podcast


class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast

        fields = [
            "feed_href",
            "podcast_name",
            "podcast_summary",
            "podcast_image",
            "podcast_twitter",
            "host",
        ]
