# Generated by Django 5.0 on 2025-02-22 11:39

import django.db.models.deletion
from django.db import migrations, models

def migrate_data(apps, schema_editor):
    VideoSource = apps.get_model('record', 'VideoSource')
    RecordingMethod = apps.get_model('record', 'RecordingMethod')
    ffmpeg = RecordingMethod.objects.create(name="ffmpeg", command='ffmpeg -user_agent "{user_agent}" -i "{video_url}" -c copy "{output_file_path}"')
    wget = RecordingMethod.objects.create(name="wget", command='wget --user-agent="{user_agent}" "{video_url}" -O "{output_file_path}"')
    for video_source in VideoSource.objects.all():
        if video_source.recording_method_old == "ffmpeg":
            video_source.recording_method_new = ffmpeg
        else:
            video_source.recording_method_new = wget
        video_source.save()

class Migration(migrations.Migration):

    dependencies = [
        ("record", "0011_alter_videosource_recording_method"),
    ]

    operations = [
        migrations.CreateModel(
            name="RecordingMethod",
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
                ("name", models.TextField(unique=True)),
                ("command", models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name="videosource",
            old_name="recording_method",
            new_name="recording_method_old",
        ),
        migrations.AddField(
            model_name="videosource",
            name="recording_method_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="video_sources",
                to="record.recordingmethod",
            ),
        ),
        migrations.RunPython(migrate_data)
    ]
