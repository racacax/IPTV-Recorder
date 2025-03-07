# Generated by Django 5.0 on 2023-12-14 15:34

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("record", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VideoSource",
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
                ("url", models.TextField()),
                ("name", models.TextField()),
                ("logo", models.TextField(null=True)),
                (
                    "recording_method",
                    models.CharField(
                        choices=[
                            ("auto", "Auto"),
                            ("wget", "wget"),
                            ("ffmpeg", "ffmpeg"),
                        ],
                        max_length=64,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="playlist",
            name="last_updated",
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0)),
        ),
        migrations.AddField(
            model_name="playlist",
            name="name",
            field=models.TextField(default="test"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="playlist",
            name="writing_directory",
            field=models.TextField(default="test"),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Recording",
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
                (
                    "start_time",
                    models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0)),
                ),
                (
                    "end_time",
                    models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0)),
                ),
                ("name", models.TextField()),
                ("gap_between_retries", models.IntegerField(default=5)),
                ("use_backup_after", models.IntegerField(default=5)),
                (
                    "last_retry",
                    models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0)),
                ),
                ("consecutive_retries", models.IntegerField(default=0)),
                ("total_retries", models.IntegerField(default=0)),
                (
                    "selected_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="record.videosource",
                    ),
                ),
                (
                    "sources",
                    models.ManyToManyField(
                        related_name="sources", to="record.videosource"
                    ),
                ),
            ],
        ),
    ]
