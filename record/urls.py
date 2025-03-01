from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token

from record import views

urlpatterns = [
    path("api/check/", views.LoggedView.as_view()),
    path("api/user/", views.UserViewSet.as_view({"get": "list"})),
    path(
        "api/playlists/",
        views.ShortPlaylistViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "api/playlists/<int:pk>/",
        views.PlaylistViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path(
        "api/recording-methods/",
        views.RecordingMethodViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "api/recording-methods/<int:pk>/",
        views.RecordingMethodViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path("api/playlists-m3u/<int:pk>/", views.PlaylistView.as_view({"get": "retrieve"})),
    path(
        "api/recordings/",
        views.RecordingViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "api/recordings/<int:pk>/",
        views.RecordingViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path(
        "api/video-sources/<int:recording_id>/",
        views.VideoSourceViewSet.as_view({"get": "list"}),
    ),
    path("api/video-sources/", views.VideoSourceViewSet.as_view({"post": "create"})),
    path(
        "api/video-source/<int:pk>/",
        views.VideoSourceViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
    ),
    path("api/token/", obtain_auth_token),
    re_path(r"^(?P<path>([^/]+/)*)$", views.MainView.as_view()),  # every pattern that doesn't correspond to API will
    # use frontend
]
