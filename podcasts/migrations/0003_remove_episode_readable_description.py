# Generated by Django 3.2.6 on 2023-04-06 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("podcasts", "0002_auto_20230406_1048"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="episode",
            name="readable_description",
        ),
    ]
