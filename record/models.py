import datetime

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


def random_file_name():
    return get_random_string(32)


class UserData(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="user_data")
    writing_directory = models.TextField()

    def __str__(self):
        return self.user.__str__()


class Playlist(models.Model):
    url = models.TextField()
    playlist_cache_file = models.TextField(default=random_file_name)
    name = models.TextField()
    last_updated = models.DateTimeField(default=datetime.datetime.fromtimestamp(0, tz=timezone.get_default_timezone()))
    refresh_gap = models.IntegerField(default=12)  # refresh every x hours
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + " (" + self.name + ")"


class Recording(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    writing_directory = models.TextField()
    start_time = models.DateTimeField(default=datetime.datetime.fromtimestamp(0, tz=timezone.get_default_timezone()))
    end_time = models.DateTimeField(default=datetime.datetime.fromtimestamp(0, tz=timezone.get_default_timezone()))
    name = models.TextField()
    gap_between_retries = models.IntegerField(default=5)  # gap in seconds
    use_backup_after = models.IntegerField(default=5)  # after how many retries do we switch to a backup source
    selected_source = models.ForeignKey("record.VideoSource", null=True, on_delete=models.SET_NULL,
                                        related_name="selected_recording")
    last_retry = models.DateTimeField(default=datetime.datetime.fromtimestamp(0, tz=timezone.get_default_timezone()))
    consecutive_retries = models.IntegerField(default=0)
    total_retries = models.IntegerField(default=0)

    class Meta:
        ordering = ("-start_time",)

    def __str__(self):
        return self.name + " (" + self.user.__str__() + ")"

class VideoSource(models.Model):
    recording = models.ForeignKey("record.Recording", on_delete=models.CASCADE, related_name="video_sources")
    url = models.TextField()
    name = models.TextField()
    logo = models.TextField(null=True)
    recording_method = models.ForeignKey("record.RecordingMethod", on_delete=models.CASCADE, related_name="video_sources")
    index = models.IntegerField(default=0)

    class Meta:
        ordering = ("index",)

class RecordingMethod(models.Model):
    name = models.TextField(unique=True)
    termination_string = models.TextField(null=True)
    command = models.TextField()
    def __str__(self):
        return self.name