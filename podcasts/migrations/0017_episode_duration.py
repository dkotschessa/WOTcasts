# Generated by Django 4.1 on 2023-08-06 09:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("podcasts", "0016_alter_episode_description_alter_episode_guid"),
    ]

    operations = [
        migrations.AddField(
            model_name="episode",
            name="duration",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]