# Generated by Django 4.1 on 2023-08-13 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("podcasts", "0017_episode_duration"),
    ]

    operations = [
        migrations.CreateModel(
            name="Channel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("feed_href", models.URLField(unique=True)),
                ("channel_name", models.CharField(max_length=100)),
                ("channel_summary", models.TextField(blank=True, null=True)),
                ("channel_image", models.URLField()),
                ("host", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="YoutubeEpisode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("pub_date", models.DateTimeField()),
                ("link", models.URLField()),
                ("image", models.URLField()),
                ("guid", models.CharField(max_length=200)),
                ("duration", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "podcast_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="podcasts.podcast",
                    ),
                ),
            ],
        ),
    ]
