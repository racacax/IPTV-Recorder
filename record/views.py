import json
import logging
import shutil
from datetime import timedelta

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, QueryDict
from django.middleware.csrf import get_token
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.views import View
from django.views.generic import TemplateView
from m3u_parser import M3uParser
from rest_framework import viewsets
from rest_framework.views import APIView

from record.models import Playlist, Recording, VideoSource, UserData
from record.serializers import UserSerializer, PlaylistSerializer, ShortPlaylistSerializer, RecordingSerializer, \
    VideoSourceSerializer
from django.conf import settings


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

    def create(self, request):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            data['user'] = self.request.user
            Playlist.objects.create(**data)
            return JsonResponse(status=200, data={"created": True})
        return JsonResponse(status=400, data={"created": False})


class ShortPlaylistViewSet(PlaylistViewSet):
    serializer_class = ShortPlaylistSerializer


class RecordingViewSet(viewsets.ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

    def get_queryset(self):
        return Recording.objects.filter(user=self.request.user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            data['user'] = self.request.user
            del data['is_running']
            del data['default_source']
            user_data = UserData.objects.get(user=self.request.user)
            data["writing_directory"] = user_data.writing_directory + slugify(data["name"] + "-" + get_random_string(8))  + "/"
            recording = Recording.objects.create(**data)
            return JsonResponse(status=200, data={"created": True, "id": recording.id})
        return JsonResponse(status=400, data={"created": False})

    def destroy(self, request, *args, **kwargs):
        try:
            shutil.rmtree(self.get_object().writing_directory)
        except Exception as e:
            logging.exception(e)
        return super().destroy(request, *args, **kwargs)


class VideoSourceViewSet(viewsets.ModelViewSet):
    queryset = VideoSource.objects.all()
    serializer_class = VideoSourceSerializer

    def get_queryset(self):
        arg = {}
        if "recording_id" in self.kwargs:
            arg = {"recording__id": self.kwargs["recording_id"]}
        return VideoSource.objects.filter(recording__user=self.request.user, **arg)

    def create(self, request, *args, **kwargs):
        if "recording_id" not in self.kwargs:
            return
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            data["recording_id"] = self.kwargs["recording_id"]
            VideoSource.objects.create(**data)
            return JsonResponse(status=200, data={"created": True})
        return JsonResponse(status=400, data={"created": False})


class PlaylistView(PlaylistViewSet):
    def retrieve(self, *args, **kwargs):
        response = super().retrieve(*args, **kwargs)
        if response.status_code == 200:
            obj: Playlist = self.get_object()
            if timezone.now() - obj.last_updated > timedelta(hours=obj.refresh_gap):
                parser = M3uParser(timeout=30, useragent=settings.USER_AGENT)
                parser.parse_m3u(obj.url, check_live=False, schemes=["http", "https", "rtsp", "udp", "rtmp", "mms"])
                with open(str(settings.BASE_DIR) + "/cache/" + obj.playlist_cache_file, "w") as f:
                    f.write(json.dumps(parser.get_list()))
                    f.close()
                obj.last_updated = timezone.now()
                obj.save()
            with open(str(settings.BASE_DIR) + "/cache/" + obj.playlist_cache_file, "r") as f:
                return JsonResponse(status=200, data=json.loads(f.read()), safe=False)
        return JsonResponse(status=response.status_code, data={"error": response.status_code})


class MainView(TemplateView):
    template_name = "index.html"


class LoggedView(APIView):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return JsonResponse(status=200, data={"message": "All good"})
        return JsonResponse(status=400, data={"message": "User not authenticated"})

