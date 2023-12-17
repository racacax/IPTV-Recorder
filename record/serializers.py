from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import routers, serializers, viewsets

from record.models import Playlist, Recording, VideoSource


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ShortPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["id", "name"]


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["id", "url", "name", "epg_url",  "last_updated", "refresh_gap"]


class RecordingSerializer(serializers.ModelSerializer):
    default_source = serializers.SerializerMethodField(method_name="get_default_source", read_only=True)
    is_running = serializers.SerializerMethodField(method_name="get_is_running", read_only=True)
    class Meta:
        model = Recording
        fields = ["id", "start_time", "end_time", "name", "gap_between_retries", "use_backup_after", "last_retry",
                  "consecutive_retries", "total_retries", "default_source", "is_running"]
        read_only_fields = ["is_running", "default_source"]

    def get_default_source(self, obj):
        if not isinstance(obj, Recording):
            return
        sources = obj.video_sources.all()
        try:
            return VideoSourceSerializer(sources[0]).data
        except IndexError:
            return None
    def get_is_running(self, obj):
        if not isinstance(obj, Recording):
            return
        return obj.start_time < timezone.now() < obj.end_time


class VideoSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSource
        fields = ["id", "url", "name", "logo", "recording_method", "index"]
