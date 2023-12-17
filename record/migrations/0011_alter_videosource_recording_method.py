# Generated by Django 5.0 on 2023-12-17 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("record", "0010_alter_recording_options_alter_videosource_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="videosource",
            name="recording_method",
            field=models.CharField(
                choices=[("wget", "wget"), ("ffmpeg", "ffmpeg")], max_length=64
            ),
        ),
    ]