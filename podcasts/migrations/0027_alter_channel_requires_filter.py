# Generated by Django 4.1 on 2023-10-28 16:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("podcasts", "0026_episode_announced_to_twitter_episode_fetched_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channel",
            name="requires_filter",
            field=models.BooleanField(null=True),
        ),
    ]
