# Generated by Django 4.1 on 2023-08-29 22:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("podcasts", "0024_alter_podcast_requires_filter"),
    ]

    operations = [
        migrations.AddField(
            model_name="channel",
            name="requires_filter",
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
