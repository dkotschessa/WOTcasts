# Generated by Django 3.2.6 on 2023-04-06 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0004_rename_description_raw_data_episode_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='episode',
            name='podcast_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcasts.podcast'),
        ),
    ]
