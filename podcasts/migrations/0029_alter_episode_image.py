# Generated by Django 4.1 on 2024-05-12 09:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("podcasts", "0028_alter_podcast_requires_filter"),
    ]

    operations = [
        migrations.AlterField(
            model_name="episode",
            name="image",
            field=models.URLField(max_length=400),
        ),
    ]
