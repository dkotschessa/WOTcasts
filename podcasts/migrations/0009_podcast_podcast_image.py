# Generated by Django 3.2.6 on 2023-04-08 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("podcasts", "0008_auto_20230408_1927"),
    ]

    operations = [
        migrations.AddField(
            model_name="podcast",
            name="podcast_image",
            field=models.URLField(default="http://image.html"),
            preserve_default=False,
        ),
    ]
