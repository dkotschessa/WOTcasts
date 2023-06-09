from django.db import models


class Podcast(models.Model):
    feed_href = models.URLField(unique=True)
    podcast_name = models.CharField(max_length = 100)
    podcast_summary = models.TextField()
    podcast_image = models.URLField()


    def __str__(self) -> str:
        return f"{self.podcast_name}"

# Create your models here.
class Episode(models.Model):
    title = models.CharField(max_length= 200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    guid = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.podcast_name}: {self.title}"
    

